from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from backend import db
from backend.models import Favourite
from backend.utils.isro_api import (
    fetch_isro_data, get_stats, FALLBACK
)
import json

api_bp = Blueprint('api', __name__)

# ── ISRO DATA ENDPOINTS ──────────────────────────────────────

@api_bp.route('/stats')
def stats():
    return jsonify(get_stats())

@api_bp.route('/spacecrafts')
def spacecrafts():
    q    = request.args.get('q', '').lower()
    year = request.args.get('year', '')
    data = fetch_isro_data('spacecrafts')
    if q:
        data = [s for s in data if q in (s.get('name','') + s.get('launch_vehicle','')).lower()]
    if year:
        data = [s for s in data if (s.get('launch_date','') or '').startswith(year)]
    return jsonify({'data': data, 'count': len(data)})

@api_bp.route('/launchers')
def launchers():
    q    = request.args.get('q', '').lower()
    data = fetch_isro_data('launchers')
    if q:
        data = [l for l in data if q in (l.get('name','') + l.get('description','')).lower()]
    return jsonify({'data': data, 'count': len(data)})

@api_bp.route('/customer_satellites')
def customer_satellites():
    q       = request.args.get('q', '').lower()
    country = request.args.get('country', '')
    data    = fetch_isro_data('customer_satellites')
    if q:
        data = [s for s in data if q in s.get('name','').lower()]
    if country:
        data = [s for s in data if s.get('country','') == country]
    return jsonify({'data': data, 'count': len(data)})

@api_bp.route('/centres')
def centres():
    data = fetch_isro_data('centres')
    return jsonify({'data': data, 'count': len(data)})

@api_bp.route('/countries')
def countries():
    cust = fetch_isro_data('customer_satellites')
    countries_list = sorted(set(s.get('country','') for s in cust if s.get('country')))
    return jsonify({'countries': countries_list})

@api_bp.route('/analytics')
def analytics():
    sc   = fetch_isro_data('spacecrafts')
    cust = fetch_isro_data('customer_satellites')
    ln   = fetch_isro_data('launchers')

    # Launches by year
    year_map = {}
    for s in sc:
        y = (s.get('launch_date') or '')[:4]
        if y.isdigit():
            year_map[y] = year_map.get(y, 0) + 1
    launches_by_year = [{'year': k, 'count': v} for k, v in sorted(year_map.items())]

    # Customer satellites by country
    country_map = {}
    for s in cust:
        c = s.get('country','')
        if c:
            country_map[c] = country_map.get(c, 0) + 1
    by_country = sorted([{'country': k, 'count': v} for k,v in country_map.items()], key=lambda x:-x['count'])

    # Mission types (inferred from name)
    types = {'Earth Observation': 0,'Communication': 0,'Navigation': 0,'Science/Exploration': 0,'Technology Demo': 0}
    for s in sc:
        n = s.get('name','').lower()
        if any(x in n for x in ['cartosat','eos','risat','resourcesat','oceansat']):
            types['Earth Observation'] += 1
        elif any(x in n for x in ['insat','gsat','kalpana']):
            types['Communication'] += 1
        elif any(x in n for x in ['irnss','navic']):
            types['Navigation'] += 1
        elif any(x in n for x in ['chandrayaan','mangalyaan','astrosat','aditya','mom']):
            types['Science/Exploration'] += 1
        else:
            types['Technology Demo'] += 1

    # Launcher flights
    launcher_flights = [
        {'name': l.get('name',''), 'flights': int(l.get('number_of_flights','0').replace('+','') or 0)}
        for l in ln
    ]

    # Decade breakdown
    decades = {}
    for s in sc:
        y = int((s.get('launch_date') or '0000')[:4] or 0)
        if y > 1970:
            d = (y // 10) * 10
            decades[d] = decades.get(d, 0) + 1
    by_decade = [{'decade': f"{k}s", 'count': v} for k,v in sorted(decades.items())]

    return jsonify({
        'launches_by_year':   launches_by_year,
        'by_country':         by_country[:12],
        'mission_types':      [{'type': k, 'count': v} for k,v in types.items()],
        'launcher_flights':   launcher_flights,
        'by_decade':          by_decade,
    })

# ── FAVOURITES ───────────────────────────────────────────────

@api_bp.route('/favourites', methods=['GET'])
@login_required
def get_favourites():
    favs = Favourite.query.filter_by(user_id=current_user.id).order_by(Favourite.saved_at.desc()).all()
    return jsonify({'favourites': [f.to_dict() for f in favs]})

@api_bp.route('/favourites', methods=['POST'])
@login_required
def add_favourite():
    data      = request.get_json()
    item_type = data.get('item_type')
    item_name = data.get('item_name')
    item_data = data.get('item_data', {})

    if not item_type or not item_name:
        return jsonify({'error': 'item_type and item_name required'}), 400

    existing = Favourite.query.filter_by(
        user_id=current_user.id, item_type=item_type, item_name=item_name
    ).first()
    if existing:
        return jsonify({'error': 'Already in favourites'}), 409

    fav = Favourite(
        user_id=current_user.id,
        item_type=item_type,
        item_name=item_name,
        item_data=json.dumps(item_data)
    )
    db.session.add(fav)
    db.session.commit()
    return jsonify({'message': 'Saved to favourites!', 'favourite': fav.to_dict()}), 201

@api_bp.route('/favourites/<int:fav_id>', methods=['DELETE'])
@login_required
def remove_favourite(fav_id):
    fav = Favourite.query.filter_by(id=fav_id, user_id=current_user.id).first()
    if not fav:
        return jsonify({'error': 'Not found'}), 404
    db.session.delete(fav)
    db.session.commit()
    return jsonify({'message': 'Removed from favourites'}), 200

@api_bp.route('/favourites/check', methods=['GET'])
@login_required
def check_favourite():
    item_type = request.args.get('item_type')
    item_name = request.args.get('item_name')
    existing = Favourite.query.filter_by(
        user_id=current_user.id, item_type=item_type, item_name=item_name
    ).first()
    return jsonify({'is_favourite': existing is not None, 'fav_id': existing.id if existing else None})

import requests, json
from datetime import datetime
from backend import db
from backend.models import LaunchCache

ISRO_BASE = "https://isro.vercel.app/api"

ENDPOINTS = {
    "spacecrafts":          f"{ISRO_BASE}/spacecrafts",
    "launchers":            f"{ISRO_BASE}/launchers",
    "customer_satellites":  f"{ISRO_BASE}/customer_satellites",
    "centres":              f"{ISRO_BASE}/centres",
}

# ── Fallback sample data (when API unreachable) ────────────────
FALLBACK = {
    "spacecrafts": [
        {"name":"Aryabhata","launch_date":"1975-04-19","launch_vehicle":"Intercosmos","launch_site":"Kapustin Yar","orbit_type":"LEO"},
        {"name":"Bhaskara I","launch_date":"1979-06-07","launch_vehicle":"Intercosmos","launch_site":"Kapustin Yar","orbit_type":"LEO"},
        {"name":"INSAT-1A","launch_date":"1982-04-10","launch_vehicle":"Delta 3910","launch_site":"Cape Canaveral","orbit_type":"GEO"},
        {"name":"IRS-1A","launch_date":"1988-03-17","launch_vehicle":"Vostok","launch_site":"Baikonur","orbit_type":"SSO"},
        {"name":"INSAT-2A","launch_date":"1992-07-10","launch_vehicle":"Ariane-4","launch_site":"Kourou","orbit_type":"GEO"},
        {"name":"IRS-P3","launch_date":"1996-03-21","launch_vehicle":"PSLV","launch_site":"SHAR","orbit_type":"SSO"},
        {"name":"KALPANA-1","launch_date":"2002-09-12","launch_vehicle":"PSLV-C4","launch_site":"SHAR","orbit_type":"GEO"},
        {"name":"EDUSAT","launch_date":"2004-09-20","launch_vehicle":"GSLV-F01","launch_site":"SHAR","orbit_type":"GEO"},
        {"name":"Chandrayaan-1","launch_date":"2008-10-22","launch_vehicle":"PSLV-C11","launch_site":"SHAR","orbit_type":"Lunar"},
        {"name":"RISAT-2","launch_date":"2009-04-20","launch_vehicle":"PSLV-C12","launch_site":"SHAR","orbit_type":"LEO"},
        {"name":"Mangalyaan (MOM)","launch_date":"2013-11-05","launch_vehicle":"PSLV-C25","launch_site":"SHAR","orbit_type":"Mars"},
        {"name":"IRNSS-1A","launch_date":"2013-07-01","launch_vehicle":"PSLV-C22","launch_site":"SHAR","orbit_type":"GEO"},
        {"name":"CARTOSAT-2","launch_date":"2007-01-10","launch_vehicle":"PSLV-C7","launch_site":"SHAR","orbit_type":"SSO"},
        {"name":"ASTROSAT","launch_date":"2015-09-28","launch_vehicle":"PSLV-C30","launch_site":"SHAR","orbit_type":"LEO"},
        {"name":"GSAT-16","launch_date":"2014-12-07","launch_vehicle":"Ariane-5","launch_site":"Kourou","orbit_type":"GEO"},
        {"name":"CARTOSAT-3","launch_date":"2019-11-27","launch_vehicle":"PSLV-C47","launch_site":"SHAR","orbit_type":"SSO"},
        {"name":"EOS-01","launch_date":"2020-11-07","launch_vehicle":"PSLV-C49","launch_site":"SHAR","orbit_type":"SSO"},
        {"name":"GSAT-30","launch_date":"2020-01-17","launch_vehicle":"Ariane-5","launch_site":"Kourou","orbit_type":"GEO"},
        {"name":"Chandrayaan-3","launch_date":"2023-07-14","launch_vehicle":"LVM3-M4","launch_site":"SHAR","orbit_type":"Lunar"},
        {"name":"Aditya-L1","launch_date":"2023-09-02","launch_vehicle":"PSLV-C57","launch_site":"SHAR","orbit_type":"L1 Halo"},
    ],
    "launchers": [
        {"name":"SLV","description":"Satellite Launch Vehicle — India's first rocket","number_of_flights":"4","status":"Retired","liftoff_thrust_kN":"258","stages":"4"},
        {"name":"ASLV","description":"Augmented Satellite Launch Vehicle","number_of_flights":"4","status":"Retired","liftoff_thrust_kN":"570","stages":"5"},
        {"name":"PSLV","description":"Polar Satellite Launch Vehicle — ISRO's workhorse rocket","number_of_flights":"60+","status":"Operational","liftoff_thrust_kN":"4848","stages":"4"},
        {"name":"GSLV Mk I","description":"Geosynchronous SLV with Russian cryogenic stage","number_of_flights":"6","status":"Retired","liftoff_thrust_kN":"6832","stages":"3"},
        {"name":"GSLV Mk II","description":"Geosynchronous SLV with indigenous cryogenic engine","number_of_flights":"9","status":"Operational","liftoff_thrust_kN":"7090","stages":"3"},
        {"name":"LVM3","description":"Launch Vehicle Mark-3 — India's heaviest rocket","number_of_flights":"6","status":"Operational","liftoff_thrust_kN":"10170","stages":"3"},
        {"name":"SSLV","description":"Small Satellite Launch Vehicle for quick missions","number_of_flights":"3","status":"Operational","liftoff_thrust_kN":"3500","stages":"3"},
    ],
    "customer_satellites": [
        {"name":"SPOT-6","country":"France","launch_date":"2012-09-09","launch_vehicle":"PSLV-C21","orbit":"SSO"},
        {"name":"Deimos-2","country":"Spain","launch_date":"2014-06-30","launch_vehicle":"PSLV-C23","orbit":"SSO"},
        {"name":"SkySat-2","country":"USA","launch_date":"2014-06-30","launch_vehicle":"PSLV-C23","orbit":"SSO"},
        {"name":"AISAT","country":"Germany","launch_date":"2014-06-30","launch_vehicle":"PSLV-C23","orbit":"SSO"},
        {"name":"LEMUR-1","country":"USA","launch_date":"2014-11-05","launch_vehicle":"PSLV-C28","orbit":"SSO"},
        {"name":"DMC3-1","country":"UK","launch_date":"2015-07-10","launch_vehicle":"PSLV-C28","orbit":"SSO"},
        {"name":"GHGSat-D","country":"Canada","launch_date":"2016-06-22","launch_vehicle":"PSLV-C34","orbit":"SSO"},
        {"name":"LAPAN-A3","country":"Indonesia","launch_date":"2016-06-22","launch_vehicle":"PSLV-C34","orbit":"SSO"},
        {"name":"Al-Farabi-1","country":"Kazakhstan","launch_date":"2017-02-15","launch_vehicle":"PSLV-C37","orbit":"SSO"},
        {"name":"BGUSAT","country":"Israel","launch_date":"2017-02-15","launch_vehicle":"PSLV-C37","orbit":"SSO"},
        {"name":"Nayif-1","country":"UAE","launch_date":"2017-02-15","launch_vehicle":"PSLV-C37","orbit":"SSO"},
        {"name":"Carbonite-2","country":"UK","launch_date":"2018-01-12","launch_vehicle":"PSLV-C40","orbit":"SSO"},
        {"name":"Lemur-2","country":"USA","launch_date":"2018-01-12","launch_vehicle":"PSLV-C40","orbit":"SSO"},
        {"name":"Tyvak-0129","country":"USA","launch_date":"2018-01-12","launch_vehicle":"PSLV-C40","orbit":"SSO"},
        {"name":"S-NET","country":"Germany","launch_date":"2018-02-12","launch_vehicle":"PSLV-C40","orbit":"SSO"},
        {"name":"ICEYE-X1","country":"Finland","launch_date":"2018-01-12","launch_vehicle":"PSLV-C40","orbit":"SSO"},
        {"name":"Astrocast-0.1","country":"Switzerland","launch_date":"2019-07-05","launch_vehicle":"PSLV-C46","orbit":"LEO"},
        {"name":"EMISAT","country":"India","launch_date":"2019-04-01","launch_vehicle":"PSLV-C45","orbit":"SSO"},
    ],
    "centres": [
        {"name":"VSSC","full_name":"Vikram Sarabhai Space Centre","location":"Thiruvananthapuram, Kerala","description":"Primary rocket development and testing centre. Develops all launch vehicles.","lat":8.5241,"lon":76.9366},
        {"name":"SDSC-SHAR","full_name":"Satish Dhawan Space Centre","location":"Sriharikota, Andhra Pradesh","description":"India's primary spaceport. All ISRO launch vehicles lift off from here.","lat":13.7199,"lon":80.2304},
        {"name":"ISAC/URSC","full_name":"U.R. Rao Satellite Centre","location":"Bengaluru, Karnataka","description":"Designs, develops, and tests all ISRO satellites and spacecraft.","lat":12.9716,"lon":77.5946},
        {"name":"SAC","full_name":"Space Applications Centre","location":"Ahmedabad, Gujarat","description":"Develops payloads for remote sensing, communication and navigation.","lat":23.0225,"lon":72.5714},
        {"name":"NRSC","full_name":"National Remote Sensing Centre","location":"Hyderabad, Telangana","description":"Acquires and processes satellite remote sensing data.","lat":17.3850,"lon":78.4867},
        {"name":"LPSC","full_name":"Liquid Propulsion Systems Centre","location":"Valiamala, Kerala","description":"Designs and develops liquid and cryogenic propulsion systems.","lat":8.5500,"lon":76.8800},
        {"name":"MCF","full_name":"Master Control Facility","location":"Hassan, Karnataka","description":"Tracks, monitors and controls ISRO's geostationary satellites.","lat":13.0033,"lon":76.0998},
        {"name":"IIST","full_name":"Indian Institute of Space Science and Technology","location":"Thiruvananthapuram, Kerala","description":"India's first space university — trains future ISRO scientists.","lat":8.5519,"lon":76.8795},
    ]
}

def fetch_isro_data(key: str) -> list:
    """Fetch from ISRO API with DB caching. Falls back to sample data."""
    endpoint = ENDPOINTS.get(key)
    if not endpoint:
        return FALLBACK.get(key, [])

    # Check DB cache
    cached = LaunchCache.query.filter_by(endpoint=key).first()
    if cached and not cached.is_stale(ttl_minutes=30):
        return json.loads(cached.data)

    # Fetch from ISRO API
    try:
        resp = requests.get(endpoint, timeout=8)
        resp.raise_for_status()
        raw = resp.json()
        # API returns {"spacecrafts": [...]} format
        data_keys = list(raw.keys())
        data = raw[data_keys[0]] if data_keys else []

        # Upsert into cache
        if cached:
            cached.data = json.dumps(data)
            cached.fetched_at = datetime.utcnow()
        else:
            cached = LaunchCache(endpoint=key, data=json.dumps(data))
            db.session.add(cached)
        db.session.commit()
        return data

    except Exception as e:
        print(f"[ISRO API] Failed to fetch '{key}': {e} — using fallback")
        return FALLBACK.get(key, [])

def get_stats() -> dict:
    """Aggregate stats for the dashboard overview cards."""
    sc   = fetch_isro_data("spacecrafts")
    ln   = fetch_isro_data("launchers")
    cust = fetch_isro_data("customer_satellites")
    ctr  = fetch_isro_data("centres")

    # Count operational launchers
    operational = sum(1 for l in ln if "op" in (l.get("status","")).lower())

    # Countries served
    countries = len(set(s.get("country","") for s in cust if s.get("country")))

    return {
        "total_spacecraft":   len(sc),
        "total_launchers":    len(ln),
        "customer_satellites": len(cust),
        "total_centres":      len(ctr),
        "operational_rockets": operational,
        "countries_served":   countries,
    }

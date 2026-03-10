from backend import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80),  unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    favourites    = db.relationship("Favourite", backref="user", lazy=True, cascade="all, delete-orphan")

    def set_password(self, p):   self.password_hash = generate_password_hash(p)
    def check_password(self, p): return check_password_hash(self.password_hash, p)
    def to_dict(self):
        return {"id":self.id,"username":self.username,"email":self.email,
                "created_at":self.created_at.isoformat(),"fav_count":len(self.favourites)}

class Favourite(db.Model):
    __tablename__ = "favourites"
    id        = db.Column(db.Integer, primary_key=True)
    user_id   = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    item_type = db.Column(db.String(50),  nullable=False)
    item_name = db.Column(db.String(200), nullable=False)
    item_data = db.Column(db.Text)
    saved_at  = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint("user_id","item_type","item_name", name="uq_user_item"),)

    def to_dict(self):
        import json
        return {"id":self.id,"item_type":self.item_type,"item_name":self.item_name,
                "item_data":json.loads(self.item_data) if self.item_data else {},"saved_at":self.saved_at.isoformat()}

class LaunchCache(db.Model):
    __tablename__ = "launch_cache"
    id         = db.Column(db.Integer, primary_key=True)
    endpoint   = db.Column(db.String(200), unique=True, nullable=False)
    data       = db.Column(db.Text, nullable=False)
    fetched_at = db.Column(db.DateTime, default=datetime.utcnow)

    def is_stale(self, ttl_minutes=30):
        return (datetime.utcnow() - self.fetched_at).total_seconds()/60 > ttl_minutes

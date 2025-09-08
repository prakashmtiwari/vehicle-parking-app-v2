from sqlalchemy import null
from vpa import app, db
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from datetime import datetime
from flask_login import UserMixin



class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    passhash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=True)
    fullname = db.Column(db.String(64), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    reservation = db.relationship('Reservation', backref='user', lazy=True)




class Parking_Lot(db.Model, UserMixin):
    __tablename__ = 'parking_lot'

    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(32), unique=True)
    price = db.Column(db.Integer(), nullable=False)
    address = db.Column(db.String(32), nullable=False)
    pin_code = db.Column(db.String(6), nullable=True)
    maximum_number_of_spots = db.Column(db.Integer, nullable=False)

    spots = db.relationship('Parking_Spot', backref='lot', lazy=True)



class Parking_Spot(db.Model, UserMixin):
    __tablename__ = 'parking_spot'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(1), nullable=False)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=True)

    reservation = db.relationship('Reservation', backref='spot', lazy=True)



class Reservation(db.Model, UserMixin):
    __tablename__ = 'reservation'

    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=True)
    vehicle_number = db.Column(db.String(16), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True)
    parking_timestamp = db.Column(db.DateTime, default=datetime.now, nullable=True)
    leaving_timestamp = db.Column(db.DateTime, default=None, nullable=True)
    amount_paid = db.Column(db.Integer, nullable=True)



with app.app_context():
    db.create_all()
    # if admin exists, else create admin
    admin = User.query.filter_by(is_admin=True).first()
    if not admin:
        password_hash = generate_password_hash('admin')
        admin = User(username='admin', passhash=password_hash, fullname='Admin', is_admin=True)
        db.session.add(admin)
        db.session.commit()

    


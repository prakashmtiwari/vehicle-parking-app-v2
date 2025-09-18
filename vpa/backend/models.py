from vpa.backend.extensions import db
from datetime import datetime



# Association table for many-to-many User <-> Role
roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True),
)


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)  # hashed password
    email = db.Column(db.String(256), unique=True, nullable=True)
    active = db.Column(db.Boolean(), default=True)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)

    # Relationships
    reservations = db.relationship("Reservation", backref="user", lazy=True)
    roles = db.relationship(
        "Role",
        secondary=roles_users,
        backref=db.backref("users", lazy="dynamic"),
    )

    def __repr__(self):
        return f"<User {self.username}>"
  

class Role(db.Model):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Role {self.name}>"


class Parking_Lot(db.Model):
    __tablename__ = 'parking_lot'

    id = db.Column(db.Integer, primary_key=True)
    prime_location_name = db.Column(db.String(32), unique=True)
    price = db.Column(db.Integer(), nullable=False)
    address = db.Column(db.String(32), nullable=False)
    pin_code = db.Column(db.String(6), nullable=True)
    maximum_number_of_spots = db.Column(db.Integer, nullable=False)

    spots = db.relationship('Parking_Spot', backref='lot', lazy=True)
 
    def __repr__(self):      
        return f"<Lot {self.id} - {self.prime_location_name} - Price {self.price}>"


class Parking_Spot(db.Model):
    __tablename__ = 'parking_spot'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(1), nullable=False)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=True)

    reservation = db.relationship('Reservation', backref='spot', lazy=True)

    def __repr__(self):
        return f"<Spot {self.id} - Status {self.status} - Lot {self.lot_id}>"       



class Reservation(db.Model):
    __tablename__ = 'reservation'

    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=True)
    vehicle_number = db.Column(db.String(16), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True)
    parking_timestamp = db.Column(db.DateTime, default=datetime.now, nullable=True)
    leaving_timestamp = db.Column(db.DateTime, default=None, nullable=True)
    amount_paid = db.Column(db.Integer, nullable=True)


    def __repr__(self):
        return f"<Reservation {self.id} - Spot {self.spot_id} - User {self.user_id}>"
    


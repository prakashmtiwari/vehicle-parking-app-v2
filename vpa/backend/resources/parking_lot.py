from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from vpa.backend.models import Parking_Lot, User
from vpa.backend.extensions import db

def is_admin(user):
    return any(role.name == "admin" for role in user.roles)

class ParkingLotListResource(Resource):
    @jwt_required()
    def get(self):
        current_user = User.query.get(get_jwt_identity()["id"])
        if not current_user or not is_admin(current_user):
            return {"message": "Forbidden"}, 403

        lots = Parking_Lot.query.all()
        return [
            {
                "id": lot.id,
                "prime_location_name": lot.prime_location_name,
                "address": lot.address,
                "price": lot.price,
                "max_spots": lot.maximum_number_of_spots,
            }
            for lot in lots
        ], 200

    @jwt_required()
    def post(self):
        current_user = User.query.get(get_jwt_identity()["id"])
        if not current_user or not is_admin(current_user):
            return {"message": "Forbidden"}, 403

        data = request.get_json()
        lot = Parking_Lot(
            prime_location_name=data["prime_location_name"],
            address=data["address"],
            price=data["price"],
            maximum_number_of_spots=data["maximum_number_of_spots"],
        )
        db.session.add(lot)
        db.session.commit()
        return {"message": "Parking lot created", "id": lot.id}, 201


class ParkingLotResource(Resource):
    @jwt_required()
    def put(self, lot_id):
        current_user = User.query.get(get_jwt_identity()["id"])
        if not current_user or not is_admin(current_user):
            return {"message": "Forbidden"}, 403

        lot = Parking_Lot.query.get_or_404(lot_id)
        data = request.get_json()
        lot.prime_location_name = data.get("prime_location_name", lot.prime_location_name)
        lot.address = data.get("address", lot.address)
        lot.price = data.get("price", lot.price)
        lot.maximum_number_of_spots = data.get("maximum_number_of_spots", lot.maximum_number_of_spots)

        db.session.commit()
        return {"message": "Parking lot updated"}, 200

    @jwt_required()
    def delete(self, lot_id):
        current_user = User.query.get(get_jwt_identity()["id"])
        if not current_user or not is_admin(current_user):
            return {"message": "Forbidden"}, 403

        lot = Parking_Lot.query.get_or_404(lot_id)
        db.session.delete(lot)
        db.session.commit()
        return {"message": "Parking lot deleted"}, 200

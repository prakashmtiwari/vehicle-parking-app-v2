from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from vpa.backend.models import Parking_Lot, User
from vpa.backend.extensions import db
from vpa.backend.utils.decorators import admin_required


def is_admin(user):
    return any(role.name == "admin" for role in user.roles)

class ParkingLotListResource(Resource):
    @jwt_required()
    @admin_required
    def get(self):
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
    @admin_required
    def post(self):
        data = request.get_json()
        try:
            assert "prime_location_name" in data
            assert "address" in data
            assert "price" in data
            assert "maximum_number_of_spots" in data
        except AssertionError:
            return {"message": "Missing required fields"}, 400
        
        try: 
            lot = Parking_Lot(
                prime_location_name=data["prime_location_name"],
                address=data["address"],
                price=data["price"],
                maximum_number_of_spots=data["maximum_number_of_spots"],
            )
            db.session.add(lot)
            db.session.commit()
            return {"message": "Parking lot created", "id": lot.id}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": "Error creating parking lot", "error": str(e)}, 500


class ParkingLotResource(Resource):
    @jwt_required()
    @admin_required
    def put(self, lot_id):
        lot = Parking_Lot.query.get_or_404(lot_id)
        data = request.get_json()
        lot.prime_location_name = data.get("prime_location_name", lot.prime_location_name)
        lot.address = data.get("address", lot.address)
        lot.price = data.get("price", lot.price)
        lot.maximum_number_of_spots = data.get("maximum_number_of_spots", lot.maximum_number_of_spots)

        db.session.commit()
        return {"message": "Parking lot updated"}, 200

    @jwt_required()
    @admin_required
    def delete(self, lot_id):
        lot = Parking_Lot.query.get_or_404(lot_id)
        db.session.delete(lot)
        db.session.commit()
        return {"message": "Parking lot deleted"}, 200

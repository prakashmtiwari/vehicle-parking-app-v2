from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from vpa.backend.models import Parking_Spot, User, Parking_Lot
from vpa.backend.extensions import db
from vpa.backend.utils.decorators import admin_required

def is_admin(user):
    return any(role.name == "admin" for role in user.roles)

class SpotListResource(Resource):
    @jwt_required()
    @admin_required
    def get(self, lot_id):
        lot = Parking_Lot.query.get_or_404(lot_id)
        spots = lot.spots 
        return [
            {
                "id": s.id,
                "status": s.status,
                "lot_id": s.lot_id
            } for s in spots
        ], 200

    @jwt_required()
    @admin_required
    def post(self):
        
        data = request.get_json()
        spot = Parking_Spot(
            status=data["status"],
            lot_id=data.get("lot_id")
        )
        db.session.add(spot)
        db.session.commit()
        return {"message": "Spot created", "id": spot.id}, 201


class SpotResource(Resource):
    @jwt_required()
    @admin_required
    def put(self, spot_id):
        spot = Parking_Spot.query.get_or_404(spot_id)
        data = request.get_json()
        spot.status = data.get("status", spot.status)
        spot.lot_id = data.get("lot_id", spot.lot_id)

        db.session.commit()
        return {"message": "Spot updated"}, 200

    @jwt_required()
    @admin_required
    def delete(self, spot_id):
        spot = Parking_Spot.query.get_or_404(spot_id)
        db.session.delete(spot)
        db.session.commit()
        return {"message": "Spot deleted"}, 200

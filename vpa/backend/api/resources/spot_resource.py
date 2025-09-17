from flask_restful import Resource, Api
from vpa import app, api
from vpa.models import db, Parking_Spot
from flask import request, jsonify


class spotResource(Resource):
    def get(self, spot_id):
        """ Get a specific spot by ID """
        spot = spot.query.get(spot_id)
        if not spot:
            return {'message': 'spot not found'}, 404

        return {
            'id': spot.id,
            'lot_id': spot.lot_id,
            'status': spot.status
        }

    def patch(self, spot_id):
        """Partially update a spot — toggles status only."""
        spot = Parking_Spot.query.get(spot_id)
        if not spot:
            return {'message': 'spot not found'}, 404    

        # Toggle status
        data = request.get_json()

        if not data or 'status' not in data:
            return {'message': 'Status is required'}, 400
        new_status = data['status']
        if new_status not in ['A', 'O']:
            return {'message': 'Invalid status. Use "A" for available or "O" for occupied.'}, 400
        spot.status = new_status
        db.session.add(spot)
        # Commit the changes to the database
        db.session.commit()

        return {'message': 'Spot status updated', 'new_status': spot.status}, 200

    def delete(self, spot_id):
        """ Delete a spot """
        spot = Parking_Spot.query.get(spot_id)
        if not spot:
            return {'message': 'spot not found'}, 404
        
        if spot.status == 'O':
            return {'message': 'Cannot delete an occupied spot'}, 400
        
        
        if len(spot.reservation) > 0:
                print(spot.reservation)
                return {'message': "This spot is asssociated with a Reservation. Delete that first."}
        

        db.session.delete(spot)
        db.session.commit()
        return {'message': 'spot deleted successfully'}
    

class spotListResource(Resource):
    def get(self):
        """ Get all spots """
        spots = Parking_Spot.query.all()
        return [{
            'id': c.id,
            'lot_id': c.lot_id,
            'status': c.status,
        } for c in spots]

    def post(self):
        """ Create a new spot """
        data = request.get_json()

        if not data or not all(k in data for k in ('lot_id', 'status')):
            return {'message': 'All data is not present.'}, 400

        new_spot = Parking_Spot(
            lot_id=data['lot_id'],
            status=data['status'],
        )
        db.session.add(new_spot)
        db.session.commit()

        return {'message': 'spot created successfully', 'id': new_spot.id}, 201

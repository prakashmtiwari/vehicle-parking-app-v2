from flask_restful import Resource, Api
from vpa import app, api
from vpa.models import db, Parking_Lot, Parking_Spot
from flask import request, jsonify



class lotResource(Resource):
    def get(self, lot_id=None):
        """ Get a list of lots or a single lot by ID """
        if lot_id:
            lot = Parking_Lot.query.get(lot_id)
            if not lot:
                return {'message': 'lot not found'}, 404
            return {
                'id': lot.id,
                'prime_location_name': lot.prime_location_name,
                'price': lot.price,
                'address': lot.address,
                'pin_code': lot.pin_code,
                'maximum_number_of_spots': lot.maximum_number_of_spots,     
                'spots': [{
                    'id': spot.id,
                    'status': spot.status
                } for spot in lot.spots]
            }
        
        lots = Parking_Lot.query.all()
        return {
            'lots': [{
                'id': lot.id,
                'prime_location_name': lot.prime_location_name,
                'price': lot.price,     
                'address': lot.address, 
                'pin_code': lot.pin_code,
                'maximum_number_of_spots': lot.maximum_number_of_spots,
                'spots': [{
                    'id': spot.id,
                    'status': spot.status
                } for spot in lot.spots]    
            } for lot in lots]
        }


    def post(self):
        """ Create a new lot """
        data = request.get_json()
        if not data or not data.get('prime_location_name') or not data.get('price') or not data.get('address') or not data.get('maximum_number_of_spots') or not data.get('pin_code'):
            return {'message': 'Data is not sufficient'}, 400
        
        new_lot = Parking_Lot(
            prime_location_name=data['prime_location_name'],
            price=data.get('price'),    
            address=data.get('address'),
            pin_code=data.get('pin_code'),  
            maximum_number_of_spots=data.get('maximum_number_of_spots', 0)  # Default to 0 if not provided
        )
        db.session.add(new_lot)
        db.session.commit()

        return {'message': 'lot created successfully', 'id': new_lot.id}, 201

    def put(self, id):
        """ Update an existing lot """
        lot = Parking_Lot.query.get(id)
        if not lot:
            return {'message': 'lot not found'}, 404
        

        data = request.get_json()
        
        if not data:
            return {'message': 'No data provided to update'}, 400

        
        if 'prime_location_name' in data:
            lot.prime_location_name = data['prime_location_name']
        if 'price' in data:
            lot.price = data['price']
        if 'address' in data:
            lot.address = data['address']
        if 'pin_code' in data:
            lot.pin_code = data['pin_code']
        if 'maximum_number_of_spots' in data:
            lot.maximum_number_of_spots = data['maximum_number_of_spots']
    
                
        db.session.add(lot)
    
        # Commit the changes to the database            

        db.session.commit()
        return {'message': 'lot updated successfully'}, 200

    def delete(self, id):
        """ Delete a lot """
        lot = Parking_Lot.query.get(id)

        if not lot:
            return {'message': 'lot not found'}, 404
        
        # Check if lot has any associated spots
        if lot.spots and  len(lot.spots) > 0:
            return {'message': 'Cannot delete this parking lot. It still has spots available.'}, 400


        db.session.delete(lot)
        db.session.commit()
        return {'message': 'lot deleted successfully'}, 200







#api.add_resource(lotResource, '/lots', '/lots/<int:lot_id>')

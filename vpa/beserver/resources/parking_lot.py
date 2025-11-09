from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from vpa.beserver.models import Parking_Lot, Parking_Spot
from vpa.beserver.extensions import db
from vpa.beserver.utils.decorators import admin_required
import logging


logger = logging.getLogger(__name__)



class ParkingLotListResource(Resource):
    @jwt_required()
    def get(self):
        lots = Parking_Lot.query.all()
        return [
            {
                "id": lot.id,
                "prime_location_name": lot.prime_location_name,
                "address": lot.address,
                "price": lot.price,
                "pin_code": lot.pin_code,
                "maximum_number_of_spots": lot.maximum_number_of_spots,
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
            assert "pin_code" in data  
            assert "maximum_number_of_spots" in data
        except AssertionError:
            return {"message": "Missing required fields"}, 400
        
        #check this parking lot with same prime_location_name already exists
        existing_lot = Parking_Lot.query.filter_by(prime_location_name=data["prime_location_name"]).first()
        if existing_lot:
            return {"message": "Parking lot with this prime location name already exists"}, 400         
        
        
        try: 
            lot = Parking_Lot(
                prime_location_name=data["prime_location_name"],
                address=data["address"],
                price=data["price"],
                pin_code=data["pin_code"],
                maximum_number_of_spots=data["maximum_number_of_spots"],
            )
            db.session.add(lot)
            db.session.commit()
            # create parking spots according to maximum_number_of_spots
            spots = lot.maximum_number_of_spots
            for spot_number in range(1, spots + 1):
                spot = Parking_Spot(
                    lot_id=lot.id,
                    status= 'A'  # A for Available
                )
                db.session.add(spot)
            db.session.commit()
            return {"message": "Parking lot and spots created", "id": lot.id}, 201 
         
          
        except Exception as e:
            db.session.rollback()
            return {"message": "Error creating parking lot", "error": str(e)}, 500
        



class ParkingLotResource(Resource):
    @jwt_required()
    @admin_required
    def get(self, lot_id):
        lot = Parking_Lot.query.get_or_404(lot_id)
        try: 
            return {
                "id": lot.id,
                "prime_location_name": lot.prime_location_name,
                "address": lot.address,
                "price": lot.price,
                "pin_code": lot.pin_code,
                "maximum_number_of_spots": lot.maximum_number_of_spots,
            }, 200  
        except Exception as e:
            return {"message": "Error fetching parking lot", "error": str(e)}, 500  
        
    @jwt_required()
    @admin_required
    def put(self, lot_id):
        lot = Parking_Lot.query.get_or_404(lot_id)
        data = request.get_json()
        lot.prime_location_name = data.get("prime_location_name", lot.prime_location_name)
        lot.address = data.get("address", lot.address)
        lot.price = data.get("price", lot.price)
        lot.pin_code = data.get("pin_code", lot.pin_code)
        lot.maximum_number_of_spots = data.get("maximum_number_of_spots", lot.maximum_number_of_spots)

#       update the number of parking spots if maximum_number_of_spots is changed
        if "maximum_number_of_spots" in data:
            current_spots = len(lot.spots)
            new_spots = data["maximum_number_of_spots"]
            if new_spots > current_spots:
                # add new spots
                for spot_number in range(current_spots + 1, new_spots + 1):
                    spot = Parking_Spot(
                        lot_id=lot.id,
                        status= 'A'  # A for Available
                    )
                    db.session.add(spot)
            elif new_spots < current_spots:
                # remove excess spots only if they are available
                spots_to_remove = lot.spots[new_spots:]
                try:
                    for spot in spots_to_remove:
                        if spot.status == 'A':  # only remove if spot is available
                            db.session.delete(spot)
                except Exception as e:
                    db.session.rollback()
                    return {"message": "Error updating parking spots", "error": str(e)}, 500            

        db.session.commit()
        return {"message": "Parking lot updated"}, 200

    @jwt_required()
    @admin_required
    def delete(self, lot_id):
        lot = Parking_Lot.query.get_or_404(lot_id)
        #check if the parking spots are available
         
        for spot in lot.spots:
            if spot.status == "O":
                return {"message": "All the parking spots are not unoccupied !!!"}, 400
            
        # delete all the spots first
        try: 
            for spot in lot.spots:
                spot = Parking_Spot.query.get_or_404(spot.id)
                db.session.delete(spot)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error delting parking spots associated with parking lot")
            return {"message": "Error delting parking spots associated with parking lot", "error": str(e)}, 500
        
        db.session.delete(lot)
        db.session.commit()
        return {"message": "Parking lot deleted"}, 200

# Import resources
from vpa.backend.resources.user import UserListResource, UserResource
from vpa.backend.resources.parking_lot import ParkingLotListResource, ParkingLotResource
from vpa.backend.resources.spots import SpotListResource, SpotResource
from vpa.backend.resources.reservation import ReservationListResource, ReservationResource, UserReservationListResource
from vpa.backend.resources.current_user import CurrentUserResource  

def register_resources(api):

    # Admin Endpoints
    # User CRUD
    api.add_resource(UserListResource, "/admin/users")
    api.add_resource(UserResource, "/admin/users/<int:user_id>")

    # Parking Lots CRUD
    api.add_resource(ParkingLotListResource, "/api/lots")
    api.add_resource(ParkingLotResource, "/api/lots/<int:lot_id>")

    # Parking Spots CRUD
    api.add_resource(SpotListResource, "/api/lots/<int:lot_id>/spots")
    api.add_resource(SpotResource, "/api/spots/<int:spot_id>")

    # Reservations CRUD
    api.add_resource(ReservationListResource, "/api/reservations")
    api.add_resource(UserReservationListResource, "/api/myreservations")
    api.add_resource(ReservationResource, "/api/reservations/<int:reservation_id>")



    # User Endpoints
    api.add_resource(CurrentUserResource, "/self")

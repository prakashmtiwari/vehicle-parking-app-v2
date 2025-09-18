# Import resources
from vpa.backend.resources.user import UserListResource, UserResource
from vpa.backend.resources.parking_lot import ParkingLotListResource, ParkingLotResource
from vpa.backend.resources.spots import SpotListResource, SpotResource
from vpa.backend.resources.admin_reservation import ReservationListResource, ReservationResource
from vpa.backend.resources.user_reservation import UserReservationListResource, UserReservationResource
from vpa.backend.resources.current_user import CurrentUserResource  

def register_resources(api):

    # Admin Endpoints
    # User CRUD
    api.add_resource(UserListResource, "/admin/users")
    api.add_resource(UserResource, "/admin/users/<int:user_id>")

    # Parking Lots CRUD
    api.add_resource(ParkingLotListResource, "/admin/lots")
    api.add_resource(ParkingLotResource, "/admin/lots/<int:lot_id>")

    # Parking Spots CRUD
    api.add_resource(SpotListResource, "/admin/spots")
    api.add_resource(SpotResource, "/admin/spots/<int:spot_id>")

    # Reservations CRUD
    api.add_resource(ReservationListResource, "/admin/reservations")
    api.add_resource(ReservationResource, "/admin/reservations/<int:reservation_id>")


    # User Endpoints
    api.add_resource(UserReservationListResource, "/reservations")
    api.add_resource(UserReservationResource, "/reservations/<int:reservation_id>")
    api.add_resource(CurrentUserResource, "/self")

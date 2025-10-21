# Import resources
from vpa.beserver.resources.user import UserListResource, UserResource
from vpa.beserver.resources.parking_lot import ParkingLotListResource, ParkingLotResource
from vpa.beserver.resources.spots import SpotListResource, SpotResource
from vpa.beserver.resources.admin_reservation import ReservationListResource
from vpa.beserver.resources.user_reservation import UserReservationListResource, UserReservationResource
from vpa.beserver.resources.current_user import CurrentUserResource  
from vpa.beserver.resources.export_user_parking_history import UserReservationHistoryResource


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
    api.add_resource(UserReservationResource, "/api/myreservations/<int:reservation_id>")

    #parking history export
    api.add_resource(UserReservationHistoryResource, "/api/export-history")

    # User Endpoints
    api.add_resource(CurrentUserResource, "/self")

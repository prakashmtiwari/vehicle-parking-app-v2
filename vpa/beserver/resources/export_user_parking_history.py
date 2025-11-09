from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from vpa.beserver.utils.decorators import user_required
from vpa.beserver.tasks.export_parking_history import export_parking_history
from flask import jsonify


class UserReservationHistoryResource(Resource):
    @jwt_required()
    @user_required
    #celery task to export user parking history
    def post(self):
        user_id = get_jwt_identity()
        job = export_parking_history.delay(user_id)

        if not job:
           return jsonify({"status": "ERROR", "message": "Job not found"}), 404
    
        return jsonify({"job_id": job.id}), 202

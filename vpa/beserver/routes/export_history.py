from flask import Blueprint, jsonify
from celery.result import AsyncResult
from vpa.beserver.scheduler.init_celery import celery
from flask_jwt_extended import get_jwt_identity, jwt_required
from vpa.beserver.utils.decorators import user_required
from vpa.beserver.tasks.export_parking_history import export_parking_history

export_bp = Blueprint("export", __name__)

@export_bp.route("/api/export-history", methods=["POST"])
@jwt_required()
@user_required
def trigger_export():
    user_id = int(get_jwt_identity())
    job = export_parking_history.delay(user_id)
    return jsonify({"job_id": job.id}), 202


@export_bp.route("/api/export-status/<job_id>")
@jwt_required()
@user_required
def export_status(job_id):
    result = AsyncResult(job_id, app=celery)
    return jsonify({
        "job_id": job_id,
        "status": result.status,
        "result": result.result if result.status == "SUCCESS" else None
    })

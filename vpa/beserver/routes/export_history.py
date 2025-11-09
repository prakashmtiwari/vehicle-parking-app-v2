from flask import Blueprint, jsonify
from celery.result import AsyncResult
from vpa.beserver.scheduler.init_celery import celery
from flask_jwt_extended import get_jwt_identity, jwt_required
from vpa.beserver.utils.decorators import user_required
from vpa.beserver.tasks.export_parking_history import export_parking_history
from flask import send_from_directory, abort
import os


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
    """Check the Celery task status for an export job"""
    result = AsyncResult(job_id, app=celery)

    if result is None:
        return jsonify({"status": "ERROR", "message": "Invalid job ID"}), 404

    # Check if the job is done
    if result.state == "SUCCESS":
        return jsonify({
            "status": "SUCCESS",
            "result": result.result  # this should include `download_url`
        })
    elif result.state == "FAILURE":
        return jsonify({
            "status": "FAILURE",
            "message": str(result.info)
        })
    else:
        # Still pending or processing
        return jsonify({"status": result.state})



@export_bp.route('/exports/<path:filename>')
def serve_export(filename):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # exports folder one level up from beserver
    EXPORT_FOLDER = os.path.join(BASE_DIR, "../../../../exports")  
    EXPORT_FOLDER = os.path.abspath(EXPORT_FOLDER)  # resolve to absolute path
    try:
        # Only serve files that actually exist in the exports folder
        return send_from_directory(EXPORT_FOLDER, filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)
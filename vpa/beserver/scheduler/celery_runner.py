from vpa import create_app
from vpa.beserver.scheduler.init_celery import celery, init_celery
import logging

logging.basicConfig(level=logging.INFO)

def make_celery_app():
    """Create Flask app and initialize Celery with it."""
    app = create_app()
    init_celery(app)
    logging.info(f"Broker URL in celery_runner: {celery.conf.broker_url}")
    logging.info(f"Result Backend in celery_runner: {celery.conf.result_backend}")
    logging.info(f"Beat Schedule in celery_runner: {celery.conf.beat_schedule}")
    return celery

# 👇 Export the Celery instance for the Celery CLI
celery_app = make_celery_app()

# Only start Celery manually if this file is run directly (not when used with `celery -A`)
if __name__ == "__main__":
    celery_app.start()

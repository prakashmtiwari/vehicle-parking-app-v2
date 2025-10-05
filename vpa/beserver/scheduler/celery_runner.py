from vpa import create_app
from vpa.beserver.scheduler.init_celery import celery

# Create and initialize Flask app
app = create_app()
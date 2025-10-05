from celery.schedules import crontab
from vpa.beserver.extensions import celery
from vpa.beserver.scheduler.scheduler import beat_schedule




def init_celery(app):
    from vpa.beserver.tasks import reminder_tasks  # make sure tasks are imported
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        timezone="Asia/Kolkata",
        beat_schedule=beat_schedule
    )


    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
            
    celery.Task = ContextTask

    return celery




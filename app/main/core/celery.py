from celery import current_app as current_celery_app
from celery import Task

def make_celery(app):
    celery = current_celery_app
    celery.config_from_object(app.config, namespace="CELERY")
    
    #Add falsk to ceelery app
    if not hasattr(celery, 'flask_app'):
        celery.flask_app = app
    celery.Task = TaskWithFlaskAppContext

    return celery


class TaskWithFlaskAppContext(Task):
    def __call__(self, *args, **kwargs):
        with self.app.flask_app.app_context():
            Task.__call__(self, *args, **kwargs)


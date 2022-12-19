import os 


basedir = os.path.abspath(os.path.dirname(__name__))

# Create the super class
class Config(object):
   SECRET_KEY = os.environ.get('SECRET_KEY')
   
   CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
   CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0")
   
   SOCKETIO_MESSAGE_QUEUE = os.environ.get(
      'SOCKETIO_MESSAGE_QUEUE',
      'redis://127.0.0.1:6379/0'
   )
   
# Create the development config
class DevelopmentConfig(Config):
   DEBUG = True
  
config_by_name = dict(
    dev=DevelopmentConfig
)

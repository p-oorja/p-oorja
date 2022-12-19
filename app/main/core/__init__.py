from flask import Flask, make_response
from .config import config_by_name


from .celery import make_celery

from ..test_module.route import test_bp

from flask_cors import CORS

from flask_celeryext import FlaskCeleryExt

from flask_socketio import SocketIO

socketio = SocketIO()
ext_celery = FlaskCeleryExt(create_celery_app=make_celery)

def create_app(config_name= 'dev'):
   app = Flask(__name__)
   CORS(app)
   app.config.from_object(config_by_name[config_name])   
   
   ext_celery.init_app(app)
   
   
   
   
   print("Starting app")
   socketio.init_app(app, message_queue=app.config['SOCKETIO_MESSAGE_QUEUE'])
   
   app.register_blueprint(test_bp)
   
   @app.shell_context_processor
   def ctx():
        return {"app": app}
    
   @app.get('/')
   def home():
      return make_response("Welcome", 200)

   return app



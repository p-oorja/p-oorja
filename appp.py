from app.main.core import create_app, ext_celery, socketio
import eventlet
eventlet.monkey_patch()

app = create_app()
celery = ext_celery.celery



print(app.config)

@app.route("/")
def hello_world():
    return "Hello, World!"
    
if __name__ == '__main__':
    socketio.run(
        app,
        debug=True,
        use_reloader=True,
        host='0.0.0.0'
    )
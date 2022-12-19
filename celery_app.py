from app.main.core import create_app, ext_celery

app = create_app()
celery = ext_celery.celery


@app.route("/")
def hello_world():
    return "Hello, World!"

@app.cli.command("celery_worker")
def celery_worker():
    from watchgod import run_process
    import subprocess

    def run_worker():
        subprocess.call(
            ["celery", "-A", "celery_app.celery", "worker", "--loglevel=debug"]
        )
    run_process("./app", run_worker)
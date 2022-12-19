from flask import Blueprint, jsonify, request
from julia import Main
from .task import test_task
import traceback

test_bp = Blueprint("test", __name__, url_prefix="/api/v1/test")

@test_bp.route("/flask", methods=["GET"])
def get():
    try:
        result = Main.eval('[x^2 for x in 0:4]')
        #return jsonify(result), 200
        print("result:", flush=True)
        print(result, flush=True)
        return jsonify({"status": "success"})
    except:
        traceback.print_exc()
        return jsonify({'error': 'error occurred'}), 400

@test_bp.route("/test_celery", methods=["GET"])
def test_celery():
    task = test_task.delay()
    return jsonify(task.task_id),200


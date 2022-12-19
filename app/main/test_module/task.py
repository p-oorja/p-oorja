from celery import shared_task
from julia import Main
import traceback

@shared_task
def test_task():
    print(test_task.request.id)
    try:
        result = Main.eval('[x^2 for x in 0:4]')
        print(result)
        return { "status" : "success"}
    except:
        traceback.print_exc()                                                             
        return { "status" : "Failed"}

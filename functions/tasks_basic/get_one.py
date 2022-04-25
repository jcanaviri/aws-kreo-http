import json

from pynamodb.exceptions import DoesNotExist

from ..models.task_basic_model import TaskBasicModel

from ..lib.response import no_data
from ..lib.headers import headers


def get_one(event, context):
    try:
        task_basic_id = event['pathParameters']['task_basic_id']
    except:
        return no_data('COULD_NOT_GET_BASIC_TASKS_ID')

    try:
        found_task = TaskBasicModel.get(hash_key=task_basic_id)
    except DoesNotExist:
        return no_data('TASK_NOT_FOUND')
    except: 
        return no_data('COULD_NOT_FIND_TASK')

    body = {
        "data": {
            "task_basic_id": found_task.task_basic_id,
            "title": found_task.title,
            "description": found_task.description
        }
    }
    response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
    return response

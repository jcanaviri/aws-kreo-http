import json

from pynamodb.exceptions import DoesNotExist, DeleteError

from ..lib.headers import headers
from ..lib.response import no_data

from ..models.task_basic_model import TaskBasicModel


def delete(event, context):
    try:
        task_basic_id = event['pathParameters']['task_basic_id']
    except:
        return no_data('COULD_NOT_GET_TASK_ID')

    try:
        found_task = TaskBasicModel.get(hash_key=task_basic_id)
    except DoesNotExist:
        return no_data('TASK_NOT_FOUND')

    try:
        found_task.delete()
    except DeleteError:
        return no_data('COULD_NOT_DELETE_TASK')

    body = {
        "data": None,
        "message": "TASK_DELETED"
    }
    response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
    return response

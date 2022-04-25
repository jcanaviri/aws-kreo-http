import json

from pynamodb.exceptions import DoesNotExist, DeleteError

from ..lib.response import response_no_data, response_no_content

from ..models.task_model import TaskModel


def delete(event, context):
    try:
        task_id = event['pathParameters']['task_id']
    except:
        return response_no_data(status_code=400, message='Could not get task_id')

    try:
        found_task = TaskModel.get(hash_key=task_id)
    except DoesNotExist:
        return response_no_data(status_code=404, message='Task not found')

    try:
        found_task.delete()
    except DeleteError:
        return response_no_data(status_code=500, message='Could not delete task')

    return response_no_content(status_code=204)

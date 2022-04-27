import json

from pynamodb.exceptions import DoesNotExist, DeleteError

from ..lib.response import response_no_data

from ..models.task_basic_model import TaskBasicModel


def delete(event, context):
    try:
        task_basic_id = event['pathParameters']['task_basic_id']
    except:
        return response_no_data(status_code=400, message='Could not get the taks_basic_id')

    try:
        found_task = TaskBasicModel.get(hash_key=task_basic_id)
    except DoesNotExist:
        return response_no_data(status_code=404, message='Task Basic not found')

    try:
        found_task.delete()
    except DeleteError:
        return response_no_data(status_code=500, message='Could not delete the task')

    return response_no_data(status_code=200, message='Delete completed successfully')

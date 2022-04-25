import json

from ..models.task_basic_model import TaskBasicModel

from ..lib.headers import headers


def get_all(event, context):
    tasks_list = []

    for task in TaskBasicModel.scan():
        curr_task = {
            "task_basic_id": task.task_basic_id,
            "title": task.title,
            "description": task.description,
        }
        tasks_list.append(curr_task)

    body = {
        "data": tasks_list
    }
    response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
    return response

import json

from ..models.task_basic_model import TaskBasicModel

from ..lib.response import response_with_data


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
    return response_with_data(status_code=200,data=body)

import json

from ..models.task_model import TaskModel

from ..lib.response import response_no_data, response_with_data


def get_all(event, context):
    tasks_list = []

    for task in TaskModel.scan():
        curr_task = {
            "task_id": task.task_id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "task_type": task.task_type,
            "company_id": task.company_id
        }
        tasks_list.append(curr_task)


    body = {
        "data": tasks_list
    }
    return response_with_data(status_code=200, data=body)

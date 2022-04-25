import json

from uuid import uuid1

from pynamodb.exceptions import DoesNotExist

from ..models.task_model import TaskModel
from ..models.company_model import CompanyModel

from ..lib.response import response_no_data, response_with_data


def create(event, context):
    try:
        body = json.loads(event['body'])

        title = body['title']
        description = body['description']
        status = body['status']
        company_id = body['company_id']
    except KeyError:
        title = event['title'] if 'title' in event else None
        description = event['description'] if 'description' in event else None
        status = event['status'] if 'status' in event else None
        company_id = event['company_id'] if 'company_id' in event else None
        
    if title is None or description is None or company_id is None:
        return response_no_data(status_code=400, message='The body fields are invalid')
    if not status:
        status = False

    # Validate the company exists
    try:
        found_company = CompanyModel.get(hash_key=company_id)
    except DoesNotExist:
        return response_no_data(status_code=404, message='Company not found')
    except: 
        return response_no_data(status_code=500, message='Could not get company')

    new_task = TaskModel(
        task_id=str(uuid1()),
        title=title,
        description=description,
        status=status,
        company_id=found_company.company_id
    )

    new_task.save()

    body = {
        "task_id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "status": new_task.status,
        "company_id": new_task.company_id
    }
    return response_with_data(status_code=201, data=body)

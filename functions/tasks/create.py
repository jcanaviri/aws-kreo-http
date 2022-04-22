import json

from uuid import uuid1

from pynamodb.exceptions import DoesNotExist

from ..models.task_model import TaskModel
from ..models.company_model import CompanyModel

from ..lib.response import no_data
from ..lib.headers import headers


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
        return no_data('BAD_REQUEST')
    if not status:
        status = False

    # Validate the company exists
    try:
        found_company = CompanyModel.get(hash_key=company_id)
    except DoesNotExist:
        return no_data('COMPANY_NOT_FOUND')
    except: 
        return no_data('COULD_NOT_FIND_COMPANY')

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
    response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
    return response

import json

from uuid import uuid1

from ..lib.response import response_no_data, response_with_data
from ..models.company_model import CompanyModel
from ..models.document_model import DocumentModel


def create(event, context):
    # form_data has two keys that handle the incoming data
    try:
        body = json.loads(event['body'])

        title = body["title"]
        description = body["description"]
        company_id = body["company_id"]
    except KeyError:
        title = event['title'] if 'title' in event else None
        description = event['description'] if 'description' in event else None
        company_id = event['company_id'] if 'company_id' in event else None

    # if the values are None
    if description is None or company_id is None:
        return response_no_data(status_code=400, message='The fields are not valid.')
        
    # Find the company
    try:
        found_company = CompanyModel.get(hash_key=company_id) 
    except:
        return response_no_data(status_code=404, message='Company not found.')
    
    new_document = DocumentModel(
        document_id=str(uuid1()),
        title=title,
        description=description,
        company_id=found_company.company_id,
    )
    new_document.save()

    body = {
        "data": {
            "document_id": new_document.document_id,
            "title": new_document.title,
            "description": new_document.description,
            "company_id": new_document.company_id,
            }
    }

    return response_with_data(status_code=201, data=body)

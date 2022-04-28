import json

from ..lib.response import response_no_data, response_with_data
from ..models.document_model import DocumentModel
from ..models.company_model import CompanyModel


def update(event, context):
    # get the company_id
    try:
        document_id = event['pathParameters']['document_id']
    except:
        return response_no_data(status_code=400, message='Could not get document_id')

    body = json.loads(event['body'])

    try:
        title = body["title"]
    except KeyError:
        title = event['title'] if 'title' in event else None
    try:
        description = body["description"]
    except KeyError:
        description = event['description'] if 'description' in event else None
    try:
        company_id = body["company_id"]
    except KeyError:
        company_id = event['company_id'] if 'company_id' in event else None
        

    for doc in DocumentModel.query(hash_key=document_id):
        if title:
            doc.title = title
        if description:
            doc.description = description
        
        if company_id:
            # Find the company
            try:
                found_company = CompanyModel.get(hash_key=company_id) 
            except:
                return response_no_data(status_code=404, message='Company not found.')
            doc.company_id = found_company.company_id
        doc.save()

        body = {
            "data": {
                "document_id": doc.document_id,
                "title": doc.title,
                "description": doc.description,
                "company_id": doc.company_id,
            }
        }
        
        return response_with_data(status_code=200, data=body)

    return response_no_data(status_code=404, message='Document not found')

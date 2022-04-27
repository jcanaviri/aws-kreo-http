from pynamodb.exceptions import DoesNotExist, DeleteError

from ..lib.response import response_no_data
from ..models.company_model import CompanyModel
from ..models.task_model import TaskModel
from ..models.document_model import DocumentModel


def delete(event, context):
    try:
        company_id = event['pathParameters']['company_id']
    except:
        return response_no_data(status_code=400, message='Could not get company_id')

    try:
        found_company = CompanyModel.get(hash_key=company_id)
    except DoesNotExist:
        return response_no_data(status_code=404, message='Company not found')

    try:
        # Delete the company and delete its tasks and its documents
        found_company.delete()

        for task in TaskModel.scan(TaskModel.company_id == found_company.company_id):
            task.delete()
            
        for doc in DocumentModel.scan(TaskModel.company_id == found_company.company_id):
            doc.delete()

    except DeleteError:
        return response_no_data(status_code=500, message='Could not delete company')

    return response_no_data(status_code=200, message='Delete completed successfully')

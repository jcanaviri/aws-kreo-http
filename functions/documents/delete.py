from pynamodb.exceptions import DoesNotExist, DeleteError

from ..lib.response import response_no_data
from ..models.document_model import DocumentModel


def delete(event, context):
    try:
        document_id = event['pathParameters']['document_id']
    except:
        return response_no_data(status_code=400, message='Could not get document_id')

    try:
        found_document = DocumentModel.get(hash_key=document_id)
    except DoesNotExist:
        return response_no_data(status_code=404, message='Document not found')

    try:
        found_document.delete()
    except DeleteError:
        return response_no_data(status_code=500, message='Could not delete document')

    return response_no_data(status_code=200, message='Delete completed successfully')

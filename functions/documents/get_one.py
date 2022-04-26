from ..lib.response import response_with_data, response_no_data

from ..models.document_model import DocumentModel


def get_one(event, context):
    # get the company_id
    try:
        document_id = event['pathParameters']['document_id']
    except:
        return response_no_data(status_code=400, message='Could not get document_id')

    for doc in DocumentModel.query(hash_key=document_id):
        body = {
            "data": {
                "document_id": doc.document_id,
                "title": doc.title,
                "description": doc.description,
                "company_id": doc.company_id,
            }
        },

        return response_with_data(status_code=200, data=body)

    return response_no_data(status_code=404, message='Document not found')

from ..lib.response import response_with_data, response_no_data

from ..models.document_model import DocumentModel


def get_documents_by_company_id(event, context):
    try:
        company_id = event['pathParameters']['company_id']
    except:
        return response_no_data(status_code=400, message='Could not get company_id')

    # Get the basic tasks
    doc_list = []
    for doc in DocumentModel.scan(DocumentModel.company_id == company_id):
        curr_doc = {
            "document_id": doc.document_id,
            "title": doc.title,
            "description": doc.description,
            "company_id": doc.company_id,
        }
        doc_list.append(curr_doc)
    body = {
        "data": doc_list
    }
    return response_with_data(status_code=200, data=body)

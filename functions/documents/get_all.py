from ..lib.response import response_with_data
from ..models.document_model import DocumentModel


def get_all(event, context):
    doc_list = []
    for doc in DocumentModel.scan():
        curr_doc = {
            "document_id": doc.document_id,
            "title": doc.title,
            "description": doc.description,
            "company_id": doc.company_id,
        }
        doc_list.append(curr_doc)

    body = {
        "data": doc_list,
    }
    return response_with_data(status_code=200, data=body)

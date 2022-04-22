import json

from pynamodb.exceptions import DoesNotExist, GetError

from ..lib.headers import headers
from ..lib.response import no_data

from ..models.staff_model import StaffModel
from ..models.company_model import CompanyModel
from ..models.user_model import UserModel


def update(event, context):
    try:
        staff_id = event['pathParameters']['staff_id']
    except:
        return no_data('COULD_NOT_GET_STAFF_ID')
    
    try:
        body = json.loads(event['body'])

        first_name = body['first_name']
        last_name = body['last_name']
        address =body['address']
        phone =body['phone']
        document_number = body['document_number']
        document_type =body['document_type']
        boss = body['boss']
        job =body['job']
        image = body['image']
        company = body['company']
    except KeyError:
        first_name = event['first_name'] if 'fist_name' in event else None
        last_name = event['last_name'] if 'last_name' in event else None
        address = event['address'] if 'address' in event else None
        phone = event['phone'] if 'phone' in event else None
        document_number = event['document_number'] if 'document_number' in event else None
        document_type = event['document_type'] if 'document_type' in event else None
        boss = event['boss'] if 'boss' in event else None
        job = event['job'] if 'job' in event else None
        image = event['first_name'] if 'fist_name' in event else None
        company = event['company'] if 'company' in event else None
    
    if first_name is None or last_name is None or address is None or phone is None or \
        document_number is None or document_type is None or boss is None or job is None or \
            image is None:
        return no_data('BAD_REQUEST')

    try:
        found_staff = StaffModel.get(hash_key=staff_id)
        
        # Update all the fields
        found_staff.first_name = first_name
        found_staff.last_name = last_name
        found_staff.address = address
        found_staff.phone = phone
        found_staff.document_number = document_number
        found_staff.document_type = document_type
        found_staff.boss = boss
        found_staff.job = job
        found_staff.image_url = image

        # If there is a company we store its _id
        for company in CompanyModel.scan(CompanyModel.name == company):
            found_staff.company_id = company.company_id
        
        found_staff.save()

        found_company = CompanyModel.get(hash_key=found_staff.company_id)
        found_user = UserModel.get(hash_key=found_staff.user_id)

        body = {
            "data": {
                "staff_id": found_staff.staff_id,
                "first_name": found_staff.first_name,
                "last_name": found_staff.last_name,
                "email": found_user.email,
                "password": found_user.password,
                "address": found_staff.address,
                "phone": found_staff.phone,
                "document_number": found_staff.document_number,
                "document_type": found_staff.document_type,
                "boss": found_staff.boss,
                "job": found_staff.job,
                "image_url": found_staff.image_url,
                "company_name": found_company.name,
                "company_id": found_staff.company_id,
                "user_id": found_staff.user_id
            },
        }

        response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
        return response
    except DoesNotExist:
        return no_data('STAFF_NOT_FOUND')
    except GetError:
        return no_data('COULD_NOT_GET_STAFF')

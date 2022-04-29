import json

from pynamodb.exceptions import DoesNotExist, GetError

from ..lib.response import response_no_data, response_with_data

from ..models.staff_model import StaffModel
from ..models.company_model import CompanyModel
from ..models.user_model import UserModel


def update(event, context):
    try:
        staff_id = event['pathParameters']['staff_id']
    except:
        return response_no_data(status_code=400, message="Could not get staff_id")
    
    try:
        body = json.loads(event['body'])

        first_name = body['first_name']
        last_name = body['last_name']
        email = body['email']
        address =body['address']
        phone =body['phone']
        document_number = body['document_number']
        document_type =body['document_type']
        boss = body['boss']
        job =body['job']
        image = body['image']
        company_id = body['company_id']
    except KeyError:
        first_name = event['first_name'] if 'fist_name' in event else None
        last_name = event['last_name'] if 'last_name' in event else None
        address = event['address'] if 'address' in event else None
        email = event['email'] if 'email' in event else None
        phone = event['phone'] if 'phone' in event else None
        document_number = event['document_number'] if 'document_number' in event else None
        document_type = event['document_type'] if 'document_type' in event else None
        boss = event['boss'] if 'boss' in event else None
        job = event['job'] if 'job' in event else None
        image = event['image'] if 'image' in event else None
        company_id = event['company_id'] if 'company_id' in event else None
    
    if first_name is None or last_name is None or address is None or email is None or phone is None or \
        document_number is None or document_type is None or boss is None or job is None or \
            image is None or company_id is None:
        return response_no_data(status_code=400, message='The body fields are not valid')

    try:
        found_staff = StaffModel.get(hash_key=staff_id)
        found_user = UserModel.get(hash_key=found_staff.user_id)
        
        # Update all the staff fields
        found_staff.first_name = first_name
        found_staff.last_name = last_name
        found_staff.address = address
        found_staff.phone = phone
        found_staff.document_number = document_number
        found_staff.document_type = document_type
        found_staff.boss = boss
        found_staff.job = job
        found_staff.image_url = image

        # If the email is already registered
        for _ in UserModel.scan(UserModel.email == email):
            return response_no_data(status_code=403, message='Email is already registered')

        # Update all the user fieds
        found_user.email = email
        found_user.save()

        # If there is a company we store its _id
        for company in CompanyModel.scan(CompanyModel.company_id == company_id):
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

        return response_with_data(status_code=200, data=body)
    except DoesNotExist:
        return response_no_data(status_code=404, message="Staff not found")
    except GetError:
        return response_no_data(status_code=500, message="Could not find staff")

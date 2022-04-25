import json

from uuid import uuid1
from werkzeug.security import generate_password_hash

from ..models.staff_model import StaffModel
from ..models.company_model import CompanyModel
from ..models.user_model import UserModel
from ..lib.response import response_no_data, response_with_data


def create(event, context):
    try:
        body = json.loads(event['body'])

        first_name = body['first_name']
        last_name = body['last_name']
        email =body['email']
        password =body['password']
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
        email = event['email'] if 'email' in event else None
        password = event['password'] if 'password' in event else None
        address = event['address'] if 'address' in event else None
        phone = event['phone'] if 'phone' in event else None
        document_number = event['document_number'] if 'document_number' in event else None
        document_type = event['document_type'] if 'document_type' in event else None
        boss = event['boss'] if 'boss' in event else None
        job = event['job'] if 'job' in event else None
        image = event['image'] if 'image' in event else None
        company = event['company'] if 'company' in event else None
    
    if first_name is None or last_name is None or email is None or password is None or\
        address is None or phone is None or document_number is None or\
        document_type is None or boss is None or job is None or image is None or company is None :
        return response_no_data(status_code=400, message='The fiels are not valid')
        
    # If the email is already registered
    for _ in UserModel.scan(UserModel.email == email):
        return response_no_data(status_code=403, message='Email is already registered')
        
    # Cannot create a new staff if the company doen't exists
    for find_company in CompanyModel.scan(CompanyModel.name == company.lower()):
        # Create a new user instance
        new_user = UserModel(
            user_id=str(uuid1()),
            email=email,
            password=generate_password_hash(password)
        )
        new_user.save()

        # Create the staff
        new_staff = StaffModel(
            staff_id=str(uuid1()),
            first_name=first_name,
            last_name=last_name,
            address=address,
            phone=phone,
            document_number=document_number,
            document_type=document_type,
            boss=boss,
            job=job,
            image_url=image,
            company_id=find_company.company_id,
            user_id=new_user.user_id
        )
        new_staff.save()

        body = {
            "staff_id": new_staff.staff_id,
            "email": new_user.email,
            "password": new_user.password,
            "first_name": new_staff.first_name,
            "last_name": new_staff.last_name,
            "email": new_user.email,
            "password": new_user.password,
            "is_active": new_user.is_active,
            "is_password_change": new_user.is_password_change,
            "address": new_staff.address,
            "phone": new_staff.phone,
            "document_number": new_staff.document_number,
            "document_type": new_staff.document_type,
            "boss": new_staff.boss,
            "job": new_staff.job,
            "image_url": new_staff.image_url,
            "created_at": str(new_user.created_at),
            "updated_at": str(new_user.updated_at),
            "company_id": new_staff.company_id,
            "company_name": find_company.name,
        }
        return response_with_data(status_code=201, data=body)

    return response_no_data(status_code=400, message='Company not found')

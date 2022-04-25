import json

from uuid import uuid1
from werkzeug.security import generate_password_hash

from ..models.user_model import UserModel
from ..lib.response import response_no_data, response_with_data

# TODO: This funciton doesn't work 😊
def register(event, context):
    # This is because in AWS event doesn't have a body
    try:
        body = json.loads(event["body"])

        email = body.get('email')
        password = body.get('password')
        first_name = body.get('first_name')
        last_name = body.get('last_name')
        is_active = body.get('is_active')
    except KeyError:
        email = event['email'] if 'email' in event else None
        password = event['password'] if 'password' in event else None
        first_name = event['first_name'] if 'first_name' in event else None
        last_name = event['last_name'] if 'last_name' in event else None
        is_active = event['is_active'] if 'is_active' in event else None

    # Validate json fields
    if type(email) != str or type(password) != str \
        or type(first_name) != str or type(last_name) != str \
        or type(is_active) != bool:
            return response_no_data(status_code=400, message='The fiels in body are not valid')
            
    # Validate if the user exists
    for _ in UserModel.query(email):
        return response_no_data(status_code=406, message='User is already registered')
        
    # Save the new user
    # we have to encrypt the password
    password = generate_password_hash(password)
 
    new_user = UserModel(
        user_id=str(uuid1()),
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        is_active=is_active
    )

    new_user.save()

    body = {
        "email": new_user.email,
        "password":new_user.password,
        "first_name":new_user.first_name,
        "last_name":new_user.last_name,
        "is_active":new_user.is_active,
        "is_password_change": new_user.is_password_change
    }
    return response_with_data(status_code=201, data=body)

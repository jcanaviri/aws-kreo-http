import json

from uuid import uuid1
from werkzeug.security import generate_password_hash

from ..models.user_model import UserModel
from ..lib.headers import headers


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
            body = {
                "data": None,
                "message": "BAD_REQUEST"
            }
            response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
            return response

    # Validate if the user exists
    for _ in UserModel.query(email):
        body = {
            "data": None,
            "message": "USER_ALREADY_REGISTERED"
        }
        response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
        return response

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

    response = {"statusCode": 200, "headers": headers, "body": json.dumps({
        "email": new_user.email,
        "password":new_user.password,
        "first_name":new_user.first_name,
        "last_name":new_user.last_name,
        "is_active":new_user.is_active,
        "is_password_change": new_user.is_password_change
    })}
    return response

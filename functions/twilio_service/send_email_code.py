import json
import os

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv

from ..lib.response import response_no_data, response_with_data
from ..models.user_model import UserModel


def send_email_code(event, context):
    # Using twilio client
    load_dotenv()

    client = Client(
        os.getenv('TWILIO_ACCOUNT_SID'),
        os.getenv('TWILIO_AUTH_TOKEN')
    )

    # Get the service_id created in twilio console
    service_id = os.getenv('TWILIO_SERVICE_ID')

    # This is because in AWS GetAway
    # event doesn't have a body
    try:
        body = json.loads(event['body'])
        email = body['email']
    except KeyError:
        email = event['email'] if 'email' in event else None
    
    if email is None or type(email) != str:
        return response_no_data(status_code=400, message='The body fields are invalid')
    
    for _ in UserModel.scan(UserModel.email == email):
        try:
            res = client \
                .verify.services(service_id) \
                .verifications.create(
                    to=email, 
                    channel="email"
                )
            body = {
                "data": {
                    "sid": res.sid,
                    "service_sid": res.service_sid,
                    "account_sid": res.account_sid,
                    "to": res.to,
                    "channel": res.channel,
                    "status": res.status,
                    "valid": res.valid,
                    "amount": res.amount,
                    "payee": res.payee,
                    "date_created": str(res.date_created),
                    "date_updated": str(res.date_updated)
                }
            }

            return response_with_data(status_code=200, data=body)
        except TwilioRestException:
            return response_no_data(status_code=500, message="Twilio cannot send the code")
    
    return response_no_data(status_code=404, message="Email not found")
    

def verify_email_code(event, context):
    # Using twilio client
    load_dotenv()

    # Creating the twilio client for verify service
    client = Client(
        os.getenv('TWILIO_ACCOUNT_SID'),
        os.getenv('TWILIO_AUTH_TOKEN')
    )
    # Get the service_id created in twilio console
    service_id = os.getenv('TWILIO_SERVICE_ID')

    try:
        body = json.loads(event['body'])

        email = body['email']
        code = body['code']
    except KeyError:
        email = event['email'] if 'email' in event else None
        code = event['code'] if 'code' in event else None

    if email is None or code is None \
        or type(email) != str or type(code) != str:
        return response_no_data(status=400, message='The body fields are invalid')


    if not isinstance(code, str):
        return response_no_data(status=400, message='The body fields are invalid')

    try:
        res = client \
            .verify.services(service_id) \
            .verification_checks.create(
                to=email, 
                code=code
            )
        body = {
            "data": {
                "sid": res.sid,
                "service_sid": res.service_sid,
                "account_sid": res.account_sid,
                "to": res.to,
                "channel": res.channel,
                "status": res.status,
                "valid": res.valid,
                "amount": res.amount,
                "payee": res.payee,
                "date_created": str(res.date_created),
                "date_updated": str(res.date_updated)
            }
        }

        return response_with_data(status_code=200, data=body)
    except TwilioRestException:
        return response_no_data(status_code=500, message="Twilio cannot verify the code")

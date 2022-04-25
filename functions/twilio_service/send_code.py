import json
import os

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv

from ..lib.response import response_no_data, response_with_data


def send_phone_code(event, context):
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

        country_code = body['country_code']
        phone_number = body['phone_number']
    except KeyError:
        country_code = event['country_code'] if 'country_code' in event else None
        phone_number = event['phone_number'] if 'phone_code' in event else None

    if country_code is None or phone_number is None \
        or type(country_code) != str or type(phone_number) != str:
        body = {
            "data": None,
            "message": "BAD_REQUEST"
        }
        return response_no_data(status=400, message='The body fields are invalid')

    try:
        res = client \
            .verify.services(service_id) \
            .verifications.create(
                to=f'+{country_code}{phone_number}', 
                channel="sms"
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


def verify_phone_code(event, context):
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
        country_code = body['country_code']
        phone = body['phone_number']
        code = body['code']
    except KeyError:
        country_code = event['country_code'] if 'country_code' in event else None
        phone = event['phone_number'] if 'phone_number' in event else None
        code = event['code'] if 'code' in event else None
    
    if country_code is None or phone_number is None or code is None\
        or type(country_code) != str or type(phone_number) != str or type(code) != str:
        return response_no_data(status=400, message='The body fields are invalid')
    
    
    if not isinstance(code, str):
        return response_no_data(status=400, message='The code is invalid')

    try:
        phone_number = f'+{country_code}{phone}'

        verification = client \
            .verify.services(service_id) \
            .verification_checks.create(
                to=phone_number, 
                code=code
            )
        body = {
            "data": {
                "sid": verification.sid,
                "service_sid": verification.service_sid,
                "account_sid": verification.account_sid,
                "to": verification.to,
                "channel": verification.channel,
                "status": verification.status,
                "valid": verification.valid,
                "date_created": str(verification.date_created),
                "date_updated": str(verification.date_updated),
                "amount": verification.amount,
                "payee": verification.payee
            }
        }

        return response_with_data(status=200, data=body)
    except TwilioRestException:
        return response_no_data(status_code=500, message="Twilio cannot verify the code")

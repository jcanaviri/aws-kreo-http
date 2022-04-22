import json
import os

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv

from ..lib.headers import headers


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
        body = {
            "data": None,
            "message": "BAD_REQUEST"
        }
        response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
        return response

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

        response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}

        return response
    except TwilioRestException:
        body = {
            "data": None,
            "message": "CAN'T_SEND_CODE"
        }

        response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
        return response


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
        body = {
            "data": None,
            "message": "BAD_REQUEST"
        }
        response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
        return response


    if not isinstance(code, str):
        response = {
            "statusCode": 400,
            "headers": headers,
            "body": None,
            "message": "INVALID_CODE"
        }
        return response

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

        response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
        return response
    except TwilioRestException:
        body = {
            "data": None,
            "message": "CAN'T_VERIFY_CODE"
        }
        response = {"statusCode": 200, "headers": headers, "body": json.dumps(body)}
        return response

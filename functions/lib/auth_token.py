import os
import jwt

from dotenv import load_dotenv


def get_token(payload):
    """Returns a new token based on payload parameter"""
    load_dotenv()
    private_key = os.getenv('SECRET_KEY')
    
    encoded = jwt.encode({"secret": payload}, private_key, algorithm="HS256")
    
    return encoded


def verify_token(token, payload):
    """Returns True if the secret token is equals to the payload"""
    load_dotenv()
    decode = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=["HS256"])
    return decode['secret'] == payload

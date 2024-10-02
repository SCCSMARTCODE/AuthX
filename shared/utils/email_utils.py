"""

"""
import os
from flask import url_for
import jwt
from flask_auth.main import api

def generate_activation_link(email: str):
    payload = {
        "email": email
    }
    token = jwt.encode(payload=payload, key=os.getenv('APP_SECRET_KEY'), algorithm='HS256')
    url = f"{api.base_url[:-1]}{url_for('Basic User Auth_basic_user_activate_account', token=token)}"
    return url


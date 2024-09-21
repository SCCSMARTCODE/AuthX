import os
import jwt
from flask import request
from functools import wraps
from datetime import datetime, timedelta, timezone


def generate_token(user_id, token_key, expiration_minutes=15):
    payload = {
        'user_id': user_id,
        'exp': datetime.now(timezone.utc) + timedelta(minutes=expiration_minutes),
        'iat': datetime.now(timezone.utc)
    }
    token = jwt.encode(payload, token_key, algorithm='HS256')
    return token


def validate_token(token, token_key):
    try:
        payload = jwt.decode(token, token_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception('Token has expired')
    except jwt.InvalidTokenError:
        raise Exception('Invalid token')


def refresh_access_token(refresh_token, token_key, refresh_token_key):
    try:
        payload = jwt.decode(refresh_token, refresh_token_key, algorithms=['HS256'])
        new_token = generate_token(payload['user_id'], token_key)
        return new_token
    except jwt.ExpiredSignatureError:
        raise Exception('Refresh token has expired')
    except jwt.InvalidTokenError:
        raise Exception('Invalid refresh token')


def revoke_token(token, blacklist_store):
    # Store the token in a blacklist database or cache
    blacklist_store.add(token)
    return True


def is_token_revoked(token, blacklist_store):
    return blacklist_store.exists(token)


def introspect_token(token, token_key):
    payload = jwt.decode(token, token_key, algorithms=['HS256'])
    return {
        'user_id': payload['user_id'],
        'issued_at': payload['iat'],
        'expires_at': payload['exp']
    }


def generate_refresh_token(user_id, refresh_token_key, expiration_days=30):
    payload = {
        'user_id': user_id,
        'exp': datetime.now(timezone.utc) + timedelta(days=expiration_days),
        'iat': datetime.now(timezone.utc)
    }
    refresh_token = jwt.encode(payload, refresh_token_key, algorithm='HS256')
    return refresh_token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {'message': 'Token is missing'}, 401

        try:
            validate_token(token, os.getenv('APP_TOKEN_KEY'))
        except Exception as e:
            return {'message': str(e)}, 401

        return f(*args, **kwargs)
    return decorated


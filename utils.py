#!/usr/bin/env python3

from datetime import datetime, timedelta
from flask import request, jsonify
from functools import wraps
import pdb
import jwt
import os

def generate_token(user_id, expires_in=600):
    """
    This function generates a JWT token for a given user ID.

    Arguments:
    @user_id:str - The unique identifier of the user for whom the token is being generated.
    @expires_in:int - The number of seconds from the current time after which the token will expire (default is 600 seconds).

    The function creates a payload dictionary containing the user ID and an expiration time. The payload
    is then encoded using a secret key stored in the environment variable 'SECRET_KEY' and the HS256 algorithm.
    The function returns the encoded JWT token as a string.
    """
    payload = {"user_id":user_id, 'exp': datetime.now()+timedelta(seconds=expires_in)}
    return jwt.encode(payload, os.environ.get('SECRET_KEY'), algorithm='HS256')

def verify_token(token):
    """
    This function verifies a given JWT token.

    Argument:
    @token:str - The JWT token to be verified.

    The function attempts to decode the token using the secret key stored in the environment variable 'SECRET_KEY' 
    and the HS256 algorithm. If the token is valid, the function extracts and returns the user ID from the token's 
    payload. If any error occurs (e.g., the token is invalid or expired), the function catches the exception and 
    returns False, indicating that the token could not be verified.
    """
    try:
        payload = jwt.decode(token, os.environ["SECRET_KEY"], algorithms='HS256')
        return payload['user_id']
    except Exception:
        return False

def jwt_required(func):
    """
    This decorator function ensures that a route requires JWT authentication.

    Argument:
    @func:def - The original function that requires JWT authentication.

    The decorator ensures that only authenticated users can access the protected route.
    """
    @wraps(func)
    def decorated(*args, **kwargs):
        from .models import User, session
        if "Authorization" in request.headers:
            if token := request.headers.get("Authorization"):
                user = session.query(User).filter(User.user_id==verify_token(token)).first()
                if user:
                    return func(user.get_user_attributes(), *args, **kwargs)
                else:
                    pdb.set_trace()
                    return False
            else:
                return jsonify({"error":"Invalid Token"}), 401
        else:
            return jsonify({"error":"Missing authorization header"}), 401
    return decorated

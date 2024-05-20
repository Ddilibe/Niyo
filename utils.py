#!/usr/bin/env python3

from datetime import datetime, timedelta
from flask import request, jsonify
from functools import wraps
import pdb
import jwt
import os

def generate_token(user_id, expires_in=600):
    payload = {"user_id":user_id, 'exp': datetime.now()+timedelta(seconds=expires_in)}
    return jwt.encode(payload, os.environ.get('SECRET_KEY'), algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, os.environ["SECRET_KEY"], algorithms='HS256')
        return payload['user_id']
    except Exception:
        return False

def jwt_required(func):
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

from functools import wraps
import hashlib
import hmac
from typing import Callable

from flask import Response, request
from yt2podcast import logger
from yt2podcast.config import settings


def token_auth():
    token = request.args.get("token", default=None, type=str)
    return token == settings.auth.token

def http_auth():
    auth = request.authorization
    if auth:
        password = auth.password

        hash_algorithm = settings.auth.hash_algorithm
        if hash_algorithm and hash_algorithm in hashlib.algorithms_available:
            hashed_password = hashlib.new(hash_algorithm, password.encode())
            return hmac.compare_digest(hashed_password.hexdigest(), settings.auth.password)
        else:
            return hmac.compare_digest(password, settings.auth.password)

    return False

def check_password():
    if settings.auth.token:
        return token_auth()
    elif settings.auth.password:
        return http_auth()
    else:
        return True

def auth(f: Callable):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if check_password():
            return f(*args, **kwargs)
        
        logger.error("Unauthorized access denied")
        return Response('Login Required', 401 )
    return wrapper
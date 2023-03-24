import json
from flask import request
from functools import wraps
import jwt

from urllib.request import urlopen
from os import environ, abort

AUTH0_DOMAIN = environ.get("AUTH0_DOMAIN", "dev-udacity-lk.eu.auth0.com")
ALGORITHMS = ["RS256"]
API_AUDIENCE = environ.get("API_AUDIENCE", "https://dacing-queen-studio.onrender.com/")


# AuthError Exception
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header
def get_token_auth_header():
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError(
            {
                "code": "authorization_header_missing",
                "description": "Authorization header is expected.",
            },
            401,
        )

    auth_parts = auth.split()

    if auth_parts[0].lower() != "bearer":
        raise AuthError(
            {
                "code": "invalid_header",
                "description": 'Authorization header must start with "Bearer".',
            },
            401,
        )
    elif len(auth_parts) == 1:
        raise AuthError(
            {"code": "invalid_header", "description": "Token not found."}, 401
        )
    elif len(auth_parts) > 2:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must be bearer token.",
            },
            401,
        )

    token = auth_parts[1]
    return token


def check_permissions(permission, payload):
    if "permissions" not in payload:
        raise AuthError(
            {
                "code": "Forbidden",
                "description": "Permission Not found",
            },
            403,
        )

    if permission not in payload["permissions"]:
        raise AuthError(
            {
                "code": "Forbidden",
                "description": "Not allowed",
            },
            403,
        )
    return True


def decode_jwt(token):
    try:
        # gets the signing key
        issuer_url = f"https://{AUTH0_DOMAIN}/"
        jwks_uri = f"{issuer_url}.well-known/jwks.json"
        jwks_client = jwt.PyJWKClient(jwks_uri)
        jwt_signing_key = jwks_client.get_signing_key_from_jwt(token).key

        payload = jwt.decode(
            token,
            key=jwt_signing_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer=issuer_url,
        )
        print("payload", payload)
        return payload

    except jwt.ExpiredSignatureError:
        raise AuthError({"code": "token_expired", "description": "Token expired."}, 401)

    except jwt.InvalidKeyError:
        raise AuthError(
            {"code": "decoded_error", "description": "Unable to decode token."}, 401
        )

    except jwt.InvalidSignatureError:
        raise AuthError(
            {"code": "invalid_signature", "description": "Invalid signature."}, 401
        )

    except jwt.InvalidAudienceError:
        raise AuthError(
            {"code": "invalid_audience", "description": "Invalid audience."}, 401
        )

    except jwt.InvalidIssuerError:
        raise AuthError(
            {"code": "invalid_issuer", "description": "Invalid issuer."}, 401
        )

    except jwt.InvalidTokenError:
        raise AuthError({"code": "invalid_token", "description": "Invalid token."}, 401)

    except Exception as InvalidAlgorithmError:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Unable to parse authentication token.",
            },
            400,
        )


"""
@requires_auth(permission) is a decorator method that:
    uses get_token_auth_header to get the token
    uses verify_decode_jwt to decode the jwt
    uses check_permissions to validate claims and check the requested permission
It returns the decorator which passes the decoded payload to the decorated method
"""


def extract_token_or_raise():
    token = get_token_auth_header()
    payload = decode_jwt(token)
    return payload


def validate_token_or_raise(permission):
    payload = extract_token_or_raise()
    check_permissions(permission, payload)
    return payload


def requires_auth(permission=""):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            payload = validate_token_or_raise(permission)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator

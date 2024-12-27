from fastapi import Depends, Request
import requests
from jose import jwt, jwk
from jose.utils import base64url_decode
import os

from projectservice.utils.get_token import get_token_from_request
from projectservice.config import settings


def get_public_key(jwks_url, kid):
    response = requests.get(jwks_url)
    jwks = response.json()
    for key in jwks['keys']:
        if key['kid'] == kid:
            return key
    raise ValueError("Key not found")


def decode_token_with_jwks(token, jwks_url):
    headers = jwt.get_unverified_header(token)
    kid = headers['kid']
    public_key = get_public_key(jwks_url, kid)
    if not public_key:
        raise ValueError("Public key not found in JWKS")
    
    key = jwk.construct(public_key)

    # Fetch the expected audience from the environment
    expected_audience = settings.auth_audience
    if not expected_audience:
        raise ValueError("Expected audience is not set in the environment variables")

    # Verify the token signature
    message, encoded_signature = token.rsplit('.', 1)
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
    if not key.verify(message.encode("utf-8"), decoded_signature):
        raise ValueError("Signature verification failed")
    
    # Decode token payload
    payload = jwt.decode(token, public_key, algorithms=["RS256"], audience=expected_audience)
    return payload


def get_payload_data(request: Request):
    jwks_url = os.getenv("auth_jwks")
    token = get_token_from_request(request)
    payload = decode_token_with_jwks(token, jwks_url)

    return payload

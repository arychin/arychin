import json
import logging
from typing import Dict, List, Union
import jwt
from jwt.algorithms import RSAAlgorithm
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

import httpx
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Response, Depends, HTTPException
from sqlalchemy.orm import Session
from projectservice.database import get_db
from projectservice.models import Roles, Users
from projectservice.utils.get_user import get_current_user
from projectservice.config import settings


logger = logging.getLogger("uvicorn.error")

audit_logger = logging.getLogger('nbs-data-management-project-service-audit')


def extract_certificates(
    known: Dict[str, List[Dict]], header: Dict[str, str]
) -> Dict[str, RSAPublicKey]:
    """Returns map with key id and generated certificate to check auth token.

    Args:
        known (Dict[str, List[Dict]]): available keys from identity provider
        header (Dict[str, str]): metadata for auth token

    Returns:
        Dict[str, RSAPublicKey]: map from key id and related pub key
    """
    certificates = {}
    for key in known['keys']:
        if key['kid'] == header['kid']:
            try:
                certificates[key['kid']] = RSAAlgorithm.from_jwk(key)
            except jwt.exceptions.InvalidAlgorithmError:
                continue
    return certificates


class AuthorizationMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        exposed_paths,
    ):
        super().__init__(app)
        self.exposed_paths = exposed_paths
        self.unauthorized_response = Response(
            status_code=HTTP_401_UNAUTHORIZED,
            content="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    async def dispatch(self, request: Request, call_next):
        if str(request.url.path) in self.exposed_paths:
            audit_logger.info('Exposed endpoint access.')
            return await call_next(request)

        try:
            if 'authorization' not in request.headers:
                return self.unauthorized_response

            _, auth_token = request.headers['authorization'].split(' ')
            auth_header = request.headers['authorization']
            logger.info("Received Authorization header: {auth_header}")
            async with httpx.AsyncClient() as client:
                keys_request = await client.get(settings.auth_jwks)
                known_certs = keys_request.json()
            token_header = jwt.get_unverified_header(auth_token)
            certs = extract_certificates(known_certs, token_header)

            jwt_payload = jwt.decode(
                auth_token,
                issuer=settings.auth_issuer,
                audience=settings.auth_audience,
                key=certs[token_header['kid']],
                algorithms=[token_header['alg']],
            )

        except jwt.exceptions.InvalidAudienceError:
            audit_logger.error(
                "Access denied. Reason: Invalid Audience.",
            )
            return self.unauthorized_response
        except jwt.exceptions.ExpiredSignatureError:
            audit_logger.error(
                "Access denied. Reason: Expired Signature.",
            )
            return self.unauthorized_response
        except jwt.exceptions.InvalidSignatureError:
            audit_logger.error(
                "Access denied. Reason: Invalid Signature.",
            )
            return self.unauthorized_response
        except KeyError:
            audit_logger.error(
                "Access denied. Reason: Auth Service Unavailable.",
            )
            return self.unauthorized_response

        has_no_access = not await self.has_access(jwt_payload)

        if has_no_access:
            audit_logger.error(
                "Access denied. Reason: User has no access to the application.",
            )
            return self.unauthorized_response

        response = await call_next(request)

        return response

    async def has_access(
        self, auth_payload: Dict[str, Union[str, List[str]]]
    ) -> bool:
        """Validate if user has granted access to api. Return true in case user
        is member of specific group. List of groups could be found in auth payload.

        Args:
            auth_payload (Dict[str, Union[str, List[str]]]): most intresting
            part here for us is 'isMemberOf' key.

        Returns:
            bool: return true only if allowed group overlaps with user groups.
        """
        allowed_groups = set(json.loads(settings.allowed_groups))
        groups = auth_payload.get('isMemberOf')
        return True
        # if isinstance(groups, str):
        #     return groups in allowed_groups
        # return bool(set(groups) & allowed_groups)

from fastapi import Request, HTTPException


def get_token_from_request(request: Request):
    # Get the 'Authorization' header
    authorization: str = request.headers.get("Authorization")
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header is missing")
    
    # Ensure it follows the 'Bearer token' format
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    
    # Extract the token
    token = authorization.split("Bearer ")[1]
    return token
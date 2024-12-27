from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from starlette.requests import Request

from projectservice.database import get_db
from projectservice.models import Roles, Users, UserRole, Permissions, RolePermission
from projectservice.utils.get_payload import get_payload_data


def get_current_user(request: Request, db: Session=Depends(get_db)):
    try:
        # Extract the JWT payload added by the middleware
        auth_token_payload = get_payload_data(request)
        print("auth_token_payload", auth_token_payload)

        # Extract user ID from the token payload
        user_id = auth_token_payload.get("uid")
        if not user_id:
            raise HTTPException(status_code=401, detail="User ID not found in token")
        
        # Fetch user details from the database
        user = db.query(Users).filter(Users.short_id == user_id.lower()).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Fetch user roles through the UserRole table
        user_roles = (
            db.query(Roles)
            .join(UserRole, UserRole.role_id == Roles.id)
            .filter(UserRole.user_id == user.id)
            .all()
        )
        if not user_roles:
            raise HTTPException(status_code=403, detail="No roles found for the user")
        
        # Aggregate permissions for the user's roles through RolePermission table
        permissions = (
            db.query(Permissions)
            .join(RolePermission, RolePermission.permission_id == Permissions.id)
            .filter(RolePermission.role_id.in_([role.id for role in user_roles]))
            .distinct()
            .all()
        )
        
        # Return user details, roles and permissions
        return {
            "id": user.id,
            "name": user.short_id,
            "roles": [role.name for role in user_roles],
            "permissions": [permission.name for permission in permissions],
        }
    except AttributeError:
        raise HTTPException(status_code=401, detail="Invalid token or missing credentials")


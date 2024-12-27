from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from projectservice.database import get_db
from projectservice.models import Roles
from projectservice.utils.get_user import get_current_user


def has_permissions(permission_name: str):
    def dependency(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
        # Query role based on the user's role
        role = db.query(Roles).filter(Roles.name.in_(user['roles'])).first()
        if not role:
            raise HTTPException(status_code=403, detail="Role not found")
        
        # Check if the user has the required permission
        permissions = [role_perm_obj.permission.name for role_perm_obj in role.permissions]
        if permission_name not in permissions:
            raise HTTPException(status_code=403, detail="Permission denied")
    return dependency
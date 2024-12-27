from pydantic import BaseModel, Field, UUID4
from datetime import date, datetime
from uuid import UUID
from typing import Optional, List


class ProjectPropertiesSchema(BaseModel):
    id: UUID
    project_id: UUID4
    name: str
    value: str
    business_entity: UUID4

    class Config: 
        orm_mode = True


# Projects schema for responses
class ProjectSchema(BaseModel):
    id: UUID
    project_id: str
    project_name: str
    state: Optional[str] = None
    country: Optional[str] = None
    created_date: date
    updated_date: date
    is_deleted: bool
    deleted_date: Optional[date] = None
    # Back reference to Parent
    data_transfer_status: UUID4
    rule_process_status: UUID4
    created_by: UUID4
    modified_by: UUID4
    deleted_by: Optional[UUID4] = None
    project_properties: List[ProjectPropertiesSchema]

    class Config: 
        orm_mode = True


# Pagination schema
class ProjectPaginationSchema(BaseModel):
    total: int
    limit: int
    offset: int
    data: List[ProjectSchema]

    class Config:
        orm_mode = True







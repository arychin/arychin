from pydantic import BaseModel, Field, UUID4
from datetime import date, datetime
from uuid import UUID
from typing import Optional, List


# Projects schema for responses
class ProjectsSchema(BaseModel):
    id: UUID
    project_id: str
    project_name: str
    project_code: str
    erf_number: str
    project_manager: Optional[str] = None
    land_owner: Optional[str] = None
    crediting_start_year: Optional[int] = Field(None, ge=1900)
    crediting_end_year: Optional[int] = Field(None, ge=1900)
    state: Optional[str] = None
    country: Optional[str] = None
    projection_system_utm: Optional[int]
    created_date: date
    updated_date: date
    is_deleted: bool
    deleted_date: Optional[date] = None
    # Back reference to Parent
    business_entity: UUID4
    methodology: UUID4
    status: UUID4
    modeling_tools: UUID4
    data_transfer_status: UUID4
    rule_process_status: UUID4
    created_by: UUID4
    modified_by: UUID4
    deleted_by: Optional[UUID4] = None

    class Config: 
        orm_mode = True


class UsersSchema(BaseModel):
    id: UUID4
    short_id: str
    created_date: date
    is_deleted: bool
    deleted_date: Optional[date]
    last_login_date_time: Optional[datetime]
    business_entity: UUID4

    class Config: 
        orm_mode = True


class BusinessEntitiesSchema(BaseModel):
    id: UUID4
    key: int 
    value: str
    description: Optional[str]

    class Config: 
        orm_mode = True


class MethodologiesSchema(BaseModel):
    id: UUID4
    key: int 
    value: str
    description: Optional[str]

    class Config: 
        orm_mode = True


class ProjectStatusSchema(BaseModel):
    id: UUID4
    key: int 
    value: str
    description: Optional[str]

    class Config: 
        orm_mode = True


class ModellingToolsSchema(BaseModel):
    id: UUID4
    key: int 
    value: str
    description: Optional[str]

    class Config: 
        orm_mode = True


class DataTransferStatusSchema(BaseModel):
    id: UUID4
    key: int 
    value: str
    description: Optional[str]

    class Config: 
        orm_mode = True


class RulesProcessStatusSchema(BaseModel):
    id: UUID4
    key: int 
    value: str
    description: Optional[str]

    class Config: 
        orm_mode = True


# Pagination schema
class ProjectPaginationSchema(BaseModel):
    total: int
    limit: int
    offset: int
    projects: List[ProjectsSchema]

    class Config:
        orm_mode = True







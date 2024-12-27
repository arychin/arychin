from typing import List, Optional
from pydantic import validator, HttpUrl, constr

from .core import (
    BaseSchema,
    ErrorSchema,
    ListPagination,
)

class ProjectData(BaseSchema):
    project_name: str = ''


class ProjectListData(ListPagination):
    result: List[ProjectData]

class ProjectListResponse(BaseSchema):
    status: str
    error: Optional[ErrorSchema]
    data: ProjectListData


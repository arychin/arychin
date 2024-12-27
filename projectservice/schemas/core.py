from pydantic import BaseModel

class BaseSchema(BaseModel):

    class Config:
        from_attributes = True

class ListPagination(BaseSchema):
    page: int
    pageSize: int
    totalRecords: int

class ErrorSchema(BaseSchema):
    code: str
    message: str

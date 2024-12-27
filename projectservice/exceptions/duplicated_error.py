import re

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import class_mapper


class DuplicatedRecordException(HTTPException):
    def __init__(self, status_code, error, model):
        self.status_code = status_code
        self.error = error
        self.model = model
        if not isinstance(self.error, str):
            self.error = self.error.orig.diag.message_detail

    def details(self):
        details = []
        error = re.search(
            r'\((?P<column>.*)\)=\((?P<value>.*)\)',
            self.error
        )
        for mapped_attr, column in class_mapper(self.model).c.items():
            if column.name == error['column']:
                details.append({
                "loc": [
                    "body",
                    mapped_attr
                ],
                "msg": f"{self.model.__name__} with {mapped_attr} `{error['value']}` already exists.",
                "type": "integrity_error"
            })
        return details


async def duplicated_record_check(request: Request, exc: DuplicatedRecordException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({
            "detail": exc.details()
        }),
    )

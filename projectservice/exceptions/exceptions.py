from fastapi import FastAPI

from projectservice.exceptions.duplicated_error import (
    DuplicatedRecordException,
    duplicated_record_check,
)

def add_exceptions_handlers(app: FastAPI):
    """Method to register all exceptions handlers in one place and
    main file littering.

    Args:
     app: FastAPI instance
    """
    app.add_exception_handler(
        DuplicatedRecordException, duplicated_record_check
    )

from typing import Any
from fastapi import FastAPI, Depends, Request, HTTPException
from app import models, dependencies, services, crud, utils

internal_app = FastAPI(
    dependencies=[
        Depends(dependencies.verify_internal_auth_token),
        Depends(dependencies.get_db),
    ],
)

internal_app.router.route_class = utils.ValidationErrorLoggingRoute


@internal_app.post("/users", response_model=models.User)
async def create_user(request: Request, payload: models.UserCreate) -> Any:
    try:
        return await services.UsersService(db=request.state.db).create_user(payload)
    except crud.EmailAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))

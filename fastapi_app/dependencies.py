from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supertokens_python.recipe.session.framework.fastapi import (
    verify_session as supertokens_verify_session,
)
from supertokens_python.recipe.session import SessionContainer
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_app import database, services, config


async def get_db(request: Request, db: AsyncSession = Depends(database.get_db)) -> None:
    request.state.db = db


token_auth_scheme = HTTPBearer()


async def get_current_user(request: Request) -> None:
    user_id = request.state.session.get_user_id()
    user = await services.UsersService(db=request.state.db).get_user_with_account(
        supertokens_id=user_id
    )
    if user is None:
        raise HTTPException(status_code=401, detail="Unauthenticated")
    request.state.current_user = user


async def require_origin_header(request: Request) -> None:
    request_origin = request.headers.get("origin")
    if request_origin is None:
        raise HTTPException(status_code=400, detail="Missing origin header")


async def verify_internal_auth_token(
    settings: config.Settings = Depends(config.get_settings),
    token: HTTPAuthorizationCredentials = Depends(token_auth_scheme),
) -> None:
    if token.credentials != settings.internal_auth_token:
        raise HTTPException(status_code=401, detail="Unauthenticated")


async def verify_session(
    request: Request,
    session: SessionContainer = Depends(supertokens_verify_session()),
) -> None:
    request.state.session = session

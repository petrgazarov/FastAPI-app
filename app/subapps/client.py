from typing import Annotated
from fastapi import (
    FastAPI,
    Depends,
    Request,
    Response,
    HTTPException,
    Header,
)
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app import services, crud, dependencies, utils, models
from app.background_tasks import calculate_event_documentation
from app.schemas import api as schemas_api

logger = utils.AppLogger.__call__().get_logger()

client_app = FastAPI(
    dependencies=[
        Depends(dependencies.get_db),
    ],
)

client_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@client_app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> Response:
    logger.error(exc)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )


client_app.router.route_class = utils.ValidationErrorLoggingRoute


@client_app.post("/events")
async def create_event(
    request: Request,
    payload: schemas_api.EventCreate,
) -> models.Event:
    account = await crud.Account(db=request.state.db).find_by(
        {"write_key": payload.write_key}
    )
    if account is None:
        raise HTTPException(status_code=404)
    event = await services.EventsService(
        db=request.state.db, account_id=account.id
    ).create_event(payload.event_data)

    calculate_event_documentation.apply_async(
        args=[account.id, event.id],
        message_properties={"MessageGroupId": account.id},
    )
    return event


@client_app.get(
    "/{write_key}/glaza.min.js",
    responses={200: {"content": {"application/javascript": {}}}},
    response_class=Response,
)
async def get_client_script(
    write_key: str,
    request: Request,
    origin: Annotated[str, Header()],
) -> Response:
    account = await crud.Account(db=request.state.db).find_by({"write_key": write_key})
    if account is None:
        raise HTTPException(status_code=404)
    domains = await crud.Domain(db=request.state.db).find_all(
        where={"account_id": account.id, "name": origin}
    )
    if len(domains) == 0:
        file_name = "domain-not-configured.min.js"
    else:
        file_name = "glaza.min.js"
    content = open(f"app/static/client/{file_name}", "r").read()
    return Response(content=content, media_type="application/javascript")

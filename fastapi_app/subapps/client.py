from fastapi import (
    FastAPI,
    Depends,
    Request,
    Response,
    HTTPException,
)
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_app import services, crud, dependencies, utils, models
from fastapi_app.background_tasks import calculate_event_documentation
from fastapi_app.schemas import api as schemas_api

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

from typing import Any, Sequence
from fastapi import FastAPI, Depends, Request
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from supertokens_python.framework.fastapi import get_middleware
from supertokens_python import get_all_cors_headers
from fastapi_app import models, services, dependencies, utils, config
from fastapi_app.utils.init_supertokens import init_supertokens
from fastapi_app.schemas import api as schemas_api
from uuid import UUID

logger = utils.AppLogger().get_logger()


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


settings = config.get_settings()

init_supertokens()

web_app = FastAPI(
    dependencies=[
        Depends(dependencies.verify_session),
        Depends(dependencies.get_db),
        Depends(dependencies.get_current_user),
    ],
    generate_unique_id_function=custom_generate_unique_id,
)

web_app.add_middleware(get_middleware())
web_app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.app_url],
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type"] + get_all_cors_headers(),
)

web_app.router.route_class = utils.ValidationErrorLoggingRoute


@web_app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(exc)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )


@web_app.get("/event_documentations", tags=["event_documentations"])
async def get_event_documentations(
    request: Request,
) -> Sequence[schemas_api.EventDocumentationsGet]:
    current_user = request.state.current_user
    event_documentations = await services.EventDocumentationsService(
        account_id=current_user.account.id, db=request.state.db
    ).get_event_documentations()

    result = [
        schemas_api.EventDocumentationsGet(
            id=event_doc.id,
            name=event_doc.name,
            last_seen=event_doc.last_seen,
            domains=event_doc.domains,
            paths=event_doc.paths,
            event_schema=schemas_api.EventDocumentationsGet_EventSchema(
                json_schema=event_doc.event_schema.json_schema
            ),
            event_documentation_examples=list(
                map(
                    lambda example: schemas_api.EventDocumentationsGet_EventDocumentationExample(
                        id=example.id,
                        event=schemas_api.EventDocumentationsGet_Event(
                            id=example.event.id,
                            name=example.event.name,
                            path=example.event.path,
                            domain=example.event.domain,
                            provider=example.event.provider,
                            properties=example.event.properties,
                            screenshot=schemas_api.EventDocumentationsGet_Screenshot(
                                id=example.event.screenshot.id,
                                image_url=example.event.screenshot.image_url(),
                            ),
                        ),
                    ),
                    event_doc.event_documentation_examples,
                )
            ),
        )
        for event_doc in event_documentations
    ]
    return result


@web_app.delete("/events/{name}", tags=["events"])
async def delete_events_by_name(name: str, request: Request) -> bool:
    current_user = request.state.current_user
    return await services.EventsService(
        account_id=current_user.account.id, db=request.state.db
    ).delete_events_by_name(name)


@web_app.delete("/events", tags=["events"])
async def delete_all_events(request: Request) -> bool:
    current_user = request.state.current_user
    return await services.EventsService(
        account_id=current_user.account.id, db=request.state.db
    ).delete_all_events()


@web_app.post("/domains", tags=["domains"])
async def create_domain(
    payload: schemas_api.DomainCreate, request: Request
) -> models.Domain:
    current_user = request.state.current_user
    domain_data = models.DomainCreate(
        name=payload.name,
        account_id=current_user.account.id,
    )
    return await services.DomainsService(
        account_id=current_user.account.id, db=request.state.db
    ).create_domain(domain_data)


@web_app.delete("/domains/{id}", tags=["domains"])
async def delete_domain(id: UUID, request: Request) -> models.Domain:
    current_user = request.state.current_user
    return await services.DomainsService(
        account_id=current_user.account.id, db=request.state.db
    ).delete_domain(id=id)


@web_app.get("/users/me", response_model=schemas_api.UserGet, tags=["users"])
async def get_current_user(request: Request) -> Any:
    return request.state.current_user


@web_app.patch("/users/me", tags=["users"])
async def update_current_user(
    request: Request, payload: schemas_api.UserUpdate
) -> models.User:
    updated_user = await services.UsersService(db=request.state.db).update_user(
        instance=request.state.current_user,
        payload=models.UserUpdate.from_orm(payload),
    )
    return updated_user


@web_app.post("/accounts", tags=["accounts"])
async def create_account(request: Request) -> models.Account:
    current_user = request.state.current_user
    account = await services.AccountsService(
        db=request.state.db, user_id=current_user.id
    ).create_account()
    update_user_data = models.UserUpdate(account_id=account.id)
    await services.UsersService(db=request.state.db).update_user(
        instance=current_user, payload=update_user_data
    )
    return account

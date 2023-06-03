import asyncio
from uuid import UUID
from app import database, services, crud, celery


@celery.celery_app.task(
    name="calculate_event_documentation",
    queue="event-documentation-updates.fifo",
)
def calculate_event_documentation(account_id: UUID, event_id: UUID) -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(calculate_event_documentation_async(account_id, event_id))
    return None


async def calculate_event_documentation_async(account_id: UUID, event_id: UUID) -> None:
    async for db in database.get_db():
        event = await crud.Event(db=db).find(event_id)

        if event:
            await services.EventDocumentationsService(
                account_id=account_id, db=db
            ).calculate_event_documentation(event=event)
        else:
            raise ValueError(f"Could not find event with id {event_id}")

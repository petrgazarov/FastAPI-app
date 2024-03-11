from typing import Sequence
from sqlalchemy import asc
from genson import SchemaBuilder  # type: ignore
from fastapi_app import crud, models
from .base import BaseService


class EventDocumentationsService(BaseService):
    async def get_event_documentations(self) -> Sequence[models.EventDocumentation]:
        return await crud.EventDocumentation(db=self.db).find_all_with_schemas(
            where={"account_id": self.account_id},
            order_by=asc(getattr(models.EventDocumentation, "name")),
        )

    async def calculate_event_documentation(
        self, event: models.Event
    ) -> models.EventDocumentation:
        event_documentation = await crud.EventDocumentation(
            db=self.db
        ).find_by_with_schema({"name": event.name, "account_id": event.account_id})
        if event_documentation is None:
            event_documentation = await self.create_event_documentation_for_event(event)
        else:
            event_documentation = await self.update_event_documentation_for_event(
                event_documentation, event
            )
        return event_documentation

    async def create_event_documentation_for_event(
        self, event: models.Event
    ) -> models.EventDocumentation:
        event_documentation = await crud.EventDocumentation(db=self.db).create(
            models.EventDocumentationCreate(
                name=event.name,
                last_seen=event.created_at,
                account_id=event.account_id,
                domains=[event.domain],
                paths=[event.path],
            )
        )
        schema_builder = SchemaBuilder()
        schema_builder.add_object(event.properties)
        await crud.EventSchema(db=self.db).create(
            models.EventSchemaCreate(
                json_schema=schema_builder.to_schema(),
                account_id=self.account_id,
                event_documentation_id=event_documentation.id,
            )
        )
        await crud.EventDocumentationExample(db=self.db).create(
            models.EventDocumentationExampleCreate(
                event_documentation_id=event_documentation.id,
                event_id=event.id,
                account_id=self.account_id,
            )
        )
        return event_documentation

    async def update_event_documentation_for_event(
        self, event_documentation: models.EventDocumentation, event: models.Event
    ) -> models.EventDocumentation:
        schema_builder = SchemaBuilder()
        schema_builder.add_schema(event_documentation.event_schema.json_schema)
        schema_builder.add_object(event.properties)
        if event.path not in event_documentation.paths:
            event_documentation.paths.append(event.path)
        if event.domain not in event_documentation.domains:
            event_documentation.domains.append(event.domain)
        await crud.EventDocumentation(db=self.db).update(
            instance=event_documentation,
            data=models.EventDocumentationUpdate(last_seen=event.created_at),
        )
        await crud.EventSchema(db=self.db).update(
            instance=event_documentation.event_schema,
            data=models.EventSchemaUpdate(json_schema=schema_builder.to_schema()),
        )

        # TODO: update EventDocumentationExamples
        return event_documentation

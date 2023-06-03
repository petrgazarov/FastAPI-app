import asyncio
from pathlib import Path
import json
from app import crud, models, database


async def run():
    db_gen = database.get_db()
    db = await anext(db_gen)
    account = await crud.Account(db=db).find_by({})
    if account is None:
        raise Exception("Must first create an account")
    path = Path(__file__).with_name("events.json")

    with path.open("r") as file:
        json_events = json.load(file)
        for json_event in json_events:
            await crud.Event(db=db).create(
                models.EventCreate(
                    name=json_event["name"],
                    path=json_event["path"],
                    domain=json_event["domain"],
                    properties=json_event["properties"],
                    account_id=account.id,
                )
            )


asyncio.run(run())

from fastapi_app import models


class DomainCreate(models.PydanticModelBase):
    name: str

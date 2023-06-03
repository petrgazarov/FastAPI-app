from app import models


class DomainCreate(models.PydanticModelBase):
    name: str

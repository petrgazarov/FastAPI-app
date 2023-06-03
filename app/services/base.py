from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4

class BaseService:
    account_id: UUID4
    db: AsyncSession
    
    def __init__(self, db: AsyncSession, account_id: UUID4):
        self.account_id = account_id
        self.db = db
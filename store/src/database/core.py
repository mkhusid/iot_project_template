from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.future import select
from config import DATABASE_URL

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True

    @classmethod
    async def select(cls, session: AsyncSession, **kwargs):
        """Selects all records from the table."""
        q = select(cls).where(*[getattr(cls, k) == v for k, v in kwargs.items()])
        result = await session.execute(q)
        return result.scalars().all()

# SQLAlchemy setup
engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncSession:
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
      
db_session = Annotated[AsyncSession, Depends(get_db)]

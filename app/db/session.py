from typing import AsyncGenerator, AsyncIterator
import contextlib


from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncConnection
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.models.v1.common import Base

async_engine: AsyncEngine = create_async_engine(
    settings.POSTGRES_ASYNC_URI, echo=False, future=True
)


local_session = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)  # type: ignore


async def async_get_db() -> AsyncGenerator[AsyncSession, None]:
    async_session = local_session

    async with async_session() as db:
        yield db
        await db.commit()

class DatabaseSessionManager:
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._sessionmaker: AsyncSession | None = None

    def init(self, host: str = settings.POSTGRES_ASYNC_URI):
        self._engine = create_async_engine(
            host, echo=False, future=True
        )
        self._sessionmaker = sessionmaker(
            bind=async_engine, class_=AsyncSession, expire_on_commit=False
        )

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


    async def create_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.drop_all)


sessionManager = DatabaseSessionManager()

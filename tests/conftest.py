import asyncio
from contextlib import ExitStack

import pytest
from fastapi.testclient import TestClient
from pytest_postgresql import factories
from pytest_postgresql.janitor import DatabaseJanitor

from app.main import start_application
from app.db.models.v1.db_user import User
from app.db.session import async_get_db, sessionManager

@pytest.fixture(autouse=True)
def app():
    with ExitStack():
        yield start_application()

@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c

test_db = factories.postgresql_proc(port=None, dbname="test_db")

@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def connection_test(test_db, event_loop):
    pg_host = test_db.host
    pg_port = test_db.port
    pg_user = test_db.user
    pg_db = test_db.dbname
    pg_password = test_db.password

    with DatabaseJanitor(
        pg_user, pg_host, pg_port, pg_db, test_db.version, pg_password
    ):
        connection_str = f"postgresql+psycopg://{pg_user}:@{pg_host}:{pg_port}/{pg_db}"
        sessionManager.init(connection_str)
        yield
        await sessionManager.close()

@pytest.fixture(scope="function", autouse=True)
async def create_tables(connection_test):
    async with sessionManager.connect() as connection:
        await sessionManager.drop_all(connection)
        await sessionManager.create_all(connection)

@pytest.fixture(scope="function", autouse=True)
async def session_override(app, connection_test):
    async def get_db_override():
        async with sessionManager.session() as session:
            yield session

    app.dependency_overrides[async_get_db] = get_db_override
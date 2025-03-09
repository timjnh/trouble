import pytest
from mongomock_motor import AsyncMongoMockClient
from beanie import init_beanie

from trouble.models import GameDocument

@pytest.fixture(autouse=True)
async def init_db():
    client = AsyncMongoMockClient()
    await init_beanie(document_models=[GameDocument], database=client.get_database(name="trouble"))
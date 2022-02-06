from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

MONGODB_URL = "mongodb://root:ChangeMe@localhost:27017"
client: AsyncIOMotorClient = None


def connect_db():
    global client
    client = AsyncIOMotorClient(MONGODB_URL)


def close_db():
    global client
    client.close()
    client = None


def get_db() -> AsyncIOMotorDatabase:
    if client is None:
        connect_db()
    return client.dsp_database

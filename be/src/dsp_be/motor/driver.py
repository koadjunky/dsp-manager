import motor.motor_asyncio


MONGODB_URL = "mongodb://root:ChangeMe@localhost:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.dsp_database

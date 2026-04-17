from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection URL
MONGO_URL = "mongodb+srv://abidharshinivimala_db_user:<db_password>@terrace-farming.vp009s8.mongodb.net/?appName=terrace-farming"

# Create client
client = AsyncIOMotorClient(MONGO_URL)

# Create database
db = client["smart_agri_db"]

# Collections (tables)
users_collection = db["users"]
monitor_collection = db["monitor"]
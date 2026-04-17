from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection URL
MONGO_URL = "mongodb://localhost:27017"

# Create client
client = AsyncIOMotorClient(MONGO_URL)

# Create database
db = client["smart_agri_db"]

# Collections (tables)
users_collection = db["users"]
monitor_collection = db["monitor"]
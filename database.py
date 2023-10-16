from motor.motor_asyncio import AsyncIOMotorClient

mc = AsyncIOMotorClient("mongodb+srv://magerpol:magerpol123@magerpol.nfwtjld.mongodb.net")

msg = mc["message"]
player = mc["player"]
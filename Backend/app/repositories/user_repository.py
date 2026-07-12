from app.config.database import db
from bson import ObjectId
from app.utils.logger import logger


class UserRepository:
    
    async def create_user(self,user:dict):
        
        logger.info("Creating new user in MongoDB")
        result = await db.users.insert_one(user)
        return result.inserted_id
    
    async def find_user_by_email(self,email:str):
        return await db.users.find_one({'email':email})
    
    async def update_user(self,user_id:str, updated_data:dict):
        logger.info("Updating user profile")
        result = await db.users.update_one(
            {'_id':ObjectId(user_id)},
            {'$set':updated_data}
        )
        return result.modified_count
    
    async def delete_user(self, user_id: str):
        logger.info("Deleting user")
        result = await db.users.delete_one(
            {"_id": ObjectId(user_id)}
        )
        return result.deleted_count
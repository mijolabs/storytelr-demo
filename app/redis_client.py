import asyncio
import aioredis


class RedisClient:
    def __init__(self, config):
        self.host = config["host"]
        self.port = config["port"]
        self.db = config["db"]
        self.password = config["password"]


    def connect(self):
        """Create the connection.
        """
        self.conn = aioredis.from_url(
            f"redis://{self.host}",
            port=self.port,
            db=self.db,
            password=self.password,
            decode_responses=True
            )
        return self.conn


    async def store_and_schedule(self, message_entry: dict) -> None:
        """Set a key and schedule expiration
        """
        set_entry = await self.conn.hset(
            message_entry["id"],
            mapping=message_entry
            )
        
        set_expiration = await self.conn.expireat(
            message_entry["id"],
            message_entry["expires"]
            )
        
    
    async def get(self, message_id: str) -> dict:
        """Retrieve a key
        """
        message = await self.conn.hgetall(message_id)
        return message


    async def time(self, message_id: str) -> dict:
        """Get Redis time
        """
        redis_time = await self.conn.time()
        return redis_time

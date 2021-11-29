import redis
from config import Config

# host='192.168.50.95'
# port=6379
class RedisOperation(object):
    def __init__(self):
        self.pool = redis.ConnectionPool(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)
        self.redis_connect = redis.Redis(connection_pool=self.pool)
import json
import random
import redis

from config.settings import DB_CONNECT, PROXY_KEY_NAME
from redis_app import logger


class RedisHelper:
    def __init__(self):
        self.client = redis.StrictRedis.from_url(DB_CONNECT)
        self.key_name = PROXY_KEY_NAME

    def create_key(self, value=""):
        try:
            self.client.set(self.key_name, value)
            return True
        except Exception as e:
            logger.error(e)
            return False

    def random_get_data(self):
        try:
            all_fields = self.client.hkeys(self.key_name)
            if all_fields:
                random_filed = random.choice(all_fields)
                value = self.client.hget(self.key_name, random_filed)
                return value
            else:
                return None
        except Exception as e:
            logger.error(e)
            return None

    def delete_a_proxy(self, proxy):
        try:
            result = self.client.hdel(self.key_name, proxy)
            if result:
                return True
            else:
                return False
        except Exception as e:
            logger.error(e)
            return False

    def batch_delete_data(self, del_data_key: list):
        try:
            self.client.hdel(self.key_name, *del_data_key)
            return True
        except Exception as e:
            logger.error(e)
            return False

    def batch_save_data(self, save_data):
        try:
            self.client.hset(self.key_name, mapping=save_data)
        except Exception as e:
            logger.error(e)

    def get_all_data(self):
        try:
            values = self.client.hgetall(self.key_name)
            if values:
                decoded_values = {k.decode('utf-8'): v.decode('utf-8') for k, v in values.items()}
                return decoded_values
            else:
                return None
        except Exception as e:
            logger.error(e)
            return None

    def clear_table(self, table_name=None):
        try:
            table = table_name if table_name else self.key_name
            self.client.delete(table)
            return True
        except Exception as e:
            logger.error(e)
            return False

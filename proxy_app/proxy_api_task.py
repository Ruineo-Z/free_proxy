import json

from proxy_app import logger
from redis_app.db_connect import RedisHelper


class ProxyApiTask:
    def __init__(self):
        self.db_helper = RedisHelper()

    def update_proxy_table(self, proxy_list):
        """
        更新保存proxy的表格，若没有表格，则新建
        :param proxy_list: 需要更新至表格的代理列表
        :return:
        """
        proxy_hash_data = {proxy_data["proxy"]: json.dumps(proxy_data) for proxy_data in proxy_list}
        try:
            self.clear_proxy_table()  # 先清空表格
            self.db_helper.batch_save_data(proxy_hash_data)
            return True
        except Exception as e:
            logger.error(e)
            return False

    def random_get_proxy(self):
        try:
            proxy_str = self.db_helper.random_get_data().decode("utf-8")
            proxy_dict = json.loads(proxy_str)
            return proxy_dict
        except Exception as e:
            logger.error(e)
            return None

    def delete_a_proxy(self, proxy):
        result = self.db_helper.delete_a_proxy(proxy)
        return result

    def get_all_proxy(self):
        all_proxy = self.db_helper.get_all_data()
        return all_proxy

    def clear_proxy_table(self):
        result = self.db_helper.clear_table()

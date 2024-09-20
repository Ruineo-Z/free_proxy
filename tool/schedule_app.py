import asyncio

from proxy_app.proxy_api_task import ProxyApiTask
from proxy_app.get_free_proxy import FreeProxy
from config.settings import PROXY_FUNC
from config import Log

logger = Log("schedule_app").log()


async def run_all_proxy():
    logger.info("开始更新ip代理池")
    try:
        proxy_helper = FreeProxy()
        task = [getattr(proxy_helper, func_name)() for func_name in PROXY_FUNC]
        await asyncio.gather(*task)

        proxy_list = proxy_helper.proxy_list
        proxy_api_task = ProxyApiTask()
        proxy_api_task.update_proxy_table(proxy_list)
        logger.info("更新ip代理池成功")
    except Exception as e:
        logger.error(f"更新ip代理池失败, Error: {e}")

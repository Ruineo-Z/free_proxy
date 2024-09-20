import asyncio
import random
from functools import wraps

import httpx

from config import Log
from config.settings import CHECK_WEB

logger = Log("http_helper").log()


class RetryOutError(Exception):
    pass


def retry(retry_times=3):
    """重试函数，用于处理请求中的网络超时情况"""

    def decorated(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            for _ in range(retry_times):
                try:
                    retry_result = await func(*args, **kwargs)
                    if _ > 0:
                        logger.info(f"重试{args}成功")
                    return retry_result
                    # return await func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"Warning: 第{_ + 1}次重试{args}, Exception: {e}")
                    await asyncio.sleep(1)  # 可选：在重试之间增加延迟
            raise RetryOutError(f"重试次数已用完! args: {args}, kwargs: {kwargs}")

        return inner

    return decorated


class HttpHelper:
    def __init__(self):
        self.proxies = None
        self.user_agent = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36'
        ]
        self._header = {
            "User-Agent": random.choice(self.user_agent),
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-CN,zh;q=0.8'
        }

    # @retry(retry_times=3)
    async def get(self, url, timeout=20, proxies=None, headers=None, params=None, ssl=False, **kwargs):
        if headers:
            self._header.update(headers)

        proxies = proxies if proxies else self.proxies
        async with httpx.AsyncClient(proxies=proxies, verify=ssl, headers=self._header, timeout=timeout) as client:
            response = await client.get(url, params=params, **kwargs)
            try:
                response.raise_for_status()
                return response
            except httpx.HTTPStatusError as http_err:
                logger.error(f"HTTP error occurred: {http_err}")  # 捕获 HTTP 错误
            except Exception as err:
                logger.error(f"Other error occurred: {err}")  # 捕获其他错误
            return None

    async def check_proxy(self, proxy):
        check_url = random.choice(CHECK_WEB)
        proxies = {
            "http://": "http://" + proxy,
            "https://": "https://" + proxy
        }
        try:
            r = await self.get(check_url, proxies=proxies, timeout=5)
            logger.info(f"Checking proxy {proxy} result {r}")
            return True
        except httpx.HTTPStatusError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
        except Exception as err:
            logger.error(f"Other error occurred: {err}")
        return False

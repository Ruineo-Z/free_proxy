import os

DB_CONNECT = "redis://redis:6379/0"
# DB_CONNECT = "redis://127.0.0.1:6379/0"

PROXY_KEY_NAME = "proxy"

PROXY_FUNC = [
    "proxy_01",
    'proxy_02',
    # 'proxy_03',
    'proxy_04',
    # 'proxy_05',
    'proxy_06',
    # 'proxy_07',
    'proxy_08',
    'proxy_09'
]

CHECK_WEB = [
    'https://www.baidu.com/',
    'https://www.qq.com/',
    'https://news.sina.com.cn/'
]


# 用于验证代理ip是否可行的网站(勿压🥺)
HTTPS_CHECK_WEB = [
    'https://www.baidu.com',
    'https://news.sina.com.cn'
]

HTTP_CHECK_WEB = [
    "http://www.9991.com",
    "http://www.eryi.org",
    "http://7999.com"
]

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')

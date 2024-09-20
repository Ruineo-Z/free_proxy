import os

DB_CONNECT = "redis://localhost:6379/0"

PROXY_KEY_NAME = "proxy"

PROXY_FUNC = [
    'proxy_02',
    # 'proxy_03',
    # 'proxy_04',
    # 'proxy_05',
    'proxy_06',
    # 'proxy_07',
    'proxy_08',
    'proxy_09'
]

CHECK_WEB = [
    'https://www.baidu.com/',
    'https://www.qq.com/',
    'https://httpbin.org/',
    'https://news.sina.com.cn/'
]

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')

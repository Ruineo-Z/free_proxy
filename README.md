# FreeProxy 免费IP代理池
**仅用于学习**

## 该项目主要功能：
- 通过爬虫定时爬取指定免费ip代理网站
- 检测代理IP可用性(通过访问指定网站进行检测)
- 可通过接口获取代理 IP
------------
## 已实现爬虫功能的免费IP代理网站
|网站名称   |代码   |
| ------------ | ------------ |
|[Free Proxy List](https://free-proxy-list.net/ "Free Proxy List")|proxy_01|
|[ProxyScrape](https://proxyscrape.com/free-proxy-list "ProxyScrape")|proxy_02   |
|  [89代理](https://www.89ip.cn/ "89代理") | proxy_04  |
|[齐云代理 ](https://proxy.ip3366.net/free/ "齐云代理 ")  | proxy_06  |
|[ 快代理](http://www.kxdaili.com/dailiip.html " 快代理")  | proxy_08  |
|[稻壳代理](https://www2.docip.net/data/free.json "稻壳代理")  | proxy_09  |
**如果有其他好的网站推荐，可以在提交在[issues](https://github.com/Ruineo-Z/free_proxy/issues "issues")中**

------------

## 开放接口
使用FastApi + Nginx搭建开放接口

| Api  | 功能  |
| ------------ | ------------ |
| /get_proxy  | 从redis数据库中，随机获取一个ip代理  |
|  /batch_get_proxy | 获取所有ip代理  |
| /delete_proxy  | 删除指定ip代理  |
| /clear_proxy_table  |清空整个ip代理数据表   |
| /refresh_proxy_table  | 刷新ip代理数据表(先清空)  |

**简易示例**
```
import requests

url = "http://127.0.0.1:8080/get_proxy"

r = requests.get(url)
print(r.json())

```
------------
## 运行项目
**克隆代码**
`git clone https://github.com/Ruineo-Z/free_proxy.git`

**安装依赖**
`pip install -r requirements.txt`

**参数配置**
```
/free_proxy/config/settings

DB_CONNECT = "redis://redis:6379/0"  # 需要链接的数据库

PROXY_FUNC = [
    "proxy_01",               # 使用的爬虫代码，可根据需要自行更新
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
    'https://www.baidu.com/',     # 用于验证代理ip是否可行的网站(勿压🥺)
    'https://www.qq.com/',
    'https://httpbin.org/',
    'https://news.sina.com.cn/'
]

```

```
/free_proxy/nginx/nginx.conf

upstream fastapi_app {
    server web:8000;                  # 'web' 是 Docker Compose 中定义的服务名称
}

server {
    listen 80;      # nginx运行的端口

```
```
/free_proxy/main

@scheduler.scheduled_job('interval', hours=3)     # 定时更新ip池间隔
```


**dokcer 运行**
```
docker-compose up --build -d
```
------------

## 部分功能介绍

#### IP代理检查
代码路径: `/free_proxy/tool/http_helper.py`

通过检查代理IP是否能狗访问指定网站判断，若需要更有针对性的检查，可修改对应代码:
```
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
```
#### IP筛选
对于已标注IP属性的网站，进行了高匿Https的筛选，并将其属性使用布尔值保存在数据库中

未标注IP属性的网站，这两个属性设置为False

## 问题反馈
有任何问题/bug，欢迎在[issues](https://github.com/Ruineo-Z/free_proxy/issues "issues")中提交
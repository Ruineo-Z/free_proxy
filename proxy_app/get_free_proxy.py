import asyncio

from bs4 import BeautifulSoup

from tool.http_helper import HttpHelper
from proxy_app import logger


class FreeProxy:
    def __init__(self, proxy=None):
        self.http_helper = HttpHelper()
        self.proxies = {'http': 'http://' + proxy, 'https': 'https://'} if proxy else None
        self.proxy_list = []
        self.lock = asyncio.Lock()

    async def update_proxy_list(self, proxy_ip, proxy_port, https, elite_proxy):
        async with self.lock:
            self.proxy_list.append(
                {
                    "proxy_ip": proxy_ip,
                    "proxy_port": proxy_port,
                    "proxy": f"{proxy_ip}:{proxy_port}",
                    "https": https,
                    "elite_proxy": elite_proxy
                }
            )

    async def check_proxy(self, proxy):
        try:
            await self.http_helper.check_proxy(proxy)
            return True
        except Exception as e:
            logger.error(e)
            return False

    async def proxy_01(self):
        """web: https://free-proxy-list.net/"""
        url = "https://free-proxy-list.net/"
        r = await self.http_helper.get(url, proxies=self.proxies)

        if r:
            html_content = r.text
            soup = BeautifulSoup(html_content, "html.parser")
            table = soup.find("table", class_="table table-striped table-bordered")
            for row in table.find_all("tr")[1:]:
                cells = [cell.get_text() for cell in row.find_all("td")]
                if cells:
                    proxy_anonymity = cells[4]
                    proxy_ip = cells[0]
                    proxy_port = cells[1]
                    proxy = f"{proxy_ip}:{proxy_port}"
                    https = cells[6]
                    check_result = False
                    if https == "yes":
                        check_result = await self.check_proxy(proxy)
                    if check_result:
                        proxy_https = True if https == "yes" else False
                        proxy_elite = True if proxy_anonymity == "elite proxy" else False
                        await self.update_proxy_list(proxy_ip, proxy_port, proxy_https, proxy_elite)

    async def proxy_02(self, limit=500):
        """web: https://proxyscrape.com/free-proxy-list"""
        url = "https://api.proxyscrape.com/v3/free-proxy-list/get"
        params = {
            "request": "getproxies",
            "skip": 0,
            "proxy_format": "protocolipport",
            "format": "json",
            "limit": limit,
            "anonymity": "Elite",
            "protocol": "socks4,socks5",
            "timeout": "5000"
        }
        r = await self.http_helper.get(url, params=params, proxies=self.proxies)

        if r:
            response_json = r.json()
            for proxy in response_json["proxies"]:
                alive = proxy["alive"]
                if alive:
                    proxy_ip = proxy["ip"]
                    proxy_port = proxy["port"]
                    proxy = f"{proxy_ip}:{proxy_port}"
                    check_result = await self.check_proxy(proxy)
                    if check_result:
                        await self.update_proxy_list(proxy_ip, proxy_port, True, True)

    # def proxy_03(self):
    #     """web: https://hide.mn/en/proxy-list/?type=s#list"""
    #     url = "https://hide.mn/en/proxy-list/?type=s#list"
    #     r = self.http_helper.get(url, proxies=self.proxies)
    #     print(r.status_code)
    #     print(r.text)

    async def proxy_04(self):
        """web: https://www.89ip.cn/"""
        # url = "https://www.89ip.cn/tqdl.html?num=500&address=&kill_address=&port=&kill_port=&isp="

        # 无法判断是否为https代理，无法判断是否为高匿代理
        all_page_number = 20
        for i in range(all_page_number):
            page_number = i + 1
            if page_number == 1:
                url = "https://www.89ip.cn/"
            else:
                url = f"https://www.89ip.cn/index_{page_number}.html"

            r = await self.http_helper.get(url, proxies=self.proxies)
            if r:
                soup = BeautifulSoup(r.text, "html.parser")
                table = soup.find("table", class_="layui-table")
                for row in table.find_all("tr")[1:]:
                    cells = [cell.get_text() for cell in row.find_all("td")]
                    if cells:
                        proxy_ip = cells[0]
                        proxy_port = cells[1]
                        proxy = f"{proxy_ip}:{proxy_port}"
                        check_result = self.check_proxy(proxy)
                        if check_result:
                            await self.update_proxy_list(proxy_ip, proxy_port, False, False)

    # 与proxy_04为一个网站，弃用
    # async def proxy_05(self, num=50):
    #     """web: https://www.89ip.cn/tqdl.html?num=500&address=&kill_address=&port=&kill_port=&isp="""
    #     url = f"https://www.89ip.cn/tqdl.html?num={num}&address=&kill_address=&port=&kill_port=&isp="
    #     r = await self.http_helper.get(url, proxies=self.proxies)
    #     if r:
    #         soup = BeautifulSoup(r.text, "html.parser")
    #         table = soup.find("div", style="padding-left:20px;")
    #         if table:
    #             # 将内容按 <br> 标签分割
    #             proxies = table.get_text(separator="\n").strip().split("\n")
    #             for proxy in proxies[:-1]:
    #                 proxy_country = ""
    #                 proxy_check_result = self.check_proxy(proxy, proxy_country)
    #                 if proxy_check_result:
    #                     print(proxy)

    async def proxy_06(self):
        """wbe: https://proxy.ip3366.net/free/"""
        """翻页: https://proxy.ip3366.net/free/?action=china&page=2"""
        all_page_number = 10
        for i in range(all_page_number):
            page_number = i + 1
            if page_number == 1:
                url = "https://proxy.ip3366.net/free/"
            else:
                url = f"https://proxy.ip3366.net/free/?action=china&page={page_number}"
            r = await self.http_helper.get(url, proxies=self.proxies)

            if r:
                soup = BeautifulSoup(r.text, "html.parser")
                table = soup.find("table", class_="table table-bordered table-striped")
                for row in table.find_all("tr")[1:]:
                    cells = [cell.get_text() for cell in row.find_all("td")]
                    if cells:
                        proxy_anonymity = cells[2]
                        proxy_https = cells[3]
                        if proxy_anonymity == "高匿" and proxy_https == "HTTPS":
                            proxy_ip = cells[0]
                            proxy_port = cells[1]
                            proxy = f"{proxy_ip}:{proxy_port}"
                            proxy_check_result = await self.check_proxy(proxy)
                            if proxy_check_result:
                                await self.update_proxy_list(proxy_ip, proxy_port, True, True)

    # def proxy_07(self, page_number=1):
    #     """web: https://www.kuaidaili.com/free/fps/"""
    #     url = f"https://www.kuaidaili.com/free/fps/{page_number}"
    #     r = self.http_helper.get(url, proxies=self.proxies)
    #     print(r.text)

    async def proxy_08(self):
        """web: http://www.kxdaili.com/dailiip.html"""
        all_page_number = 10
        for i in range(all_page_number):
            page_number = i + 1
            url = f"http://www.kxdaili.com/dailiip/1/{page_number}.html"
            r = await self.http_helper.get(url, proxies=self.proxies)
            if r:
                soup = BeautifulSoup(r.text, "html.parser")
                table = soup.find("table", class_="active")
                for row in table.find_all("tr")[1:]:
                    cells = [cell.get_text() for cell in row.find_all("td")]
                    if cells:
                        proxy_anonymity = cells[2]
                        proxy_https = cells[3]
                        if proxy_anonymity == "高匿" and proxy_https == "HTTP,HTTPS":
                            proxy_ip = cells[0]
                            proxy_port = cells[1]
                            proxy = f"{proxy_ip}:{proxy_port}"
                            proxy_check_result = await self.check_proxy(proxy)
                            if proxy_check_result:
                                await self.update_proxy_list(proxy_ip, proxy_port, True, True)

    async def proxy_09(self):
        """web: https://www.docip.net/free"""
        url = "https://www2.docip.net/data/free.json"
        r = await self.http_helper.get(url, proxies=self.proxies)

        if r:
            response_json = r.json().get("data", [])
            if response_json:
                for proxy_data in response_json:
                    proxy_https = proxy_data["proxy_type"]
                    if proxy_https == "1":  # 1为https, 2为http
                        proxy = proxy_data["ip"]
                        proxy_check_result = await self.check_proxy(proxy)
                        if proxy_check_result:
                            proxy_ip = proxy.split(":")[0]
                            proxy_port = proxy.split(":")[1]
                            await self.update_proxy_list(proxy_ip, proxy_port, True, True)

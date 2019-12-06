import random

import requests


class SpiderBase:
    proxies_url = "http://mxwhj124.v4.dailiyun.com/query.txt?key=NPD91439B6&word=&count=1000&rand=true&detail=false"
    ips = []

    def get_ips(self):
        r = requests.get(self.proxies_url)
        res = r.content.decode()
        res = res.split('\r\n')
        for i in res:
            self.ips.append(i)

    @property
    def random_proxy(self):
        self.get_ips()
        ip = random.choice(self.ips)
        ip = ip.split(":")
        proxyaddr = ip[0]
        proxyport = int(ip[1])
        proxyusernm = "mxwhj124"
        proxypasswd = "mxwhj124"
        proxyurl = "http://" + proxyusernm + ":" + proxypasswd + "@" + proxyaddr + ":" + "%d" % proxyport
        proxy = {"http": proxyurl, "https": proxyurl}
        return proxy


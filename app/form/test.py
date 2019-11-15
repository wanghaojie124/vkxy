import requests
from bs4 import BeautifulSoup

assess_list_url = 'http://jwc.swjtu.edu.cn/vatuu/AssessAction?setAction=list'
headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
                "Referer": "http://jwc.swjtu.edu.cn/vatuu/AssessAction?setAction=list",
                "X-Requested-With": "XMLHttpRequest",
                "Cookie": "Hm_lvt_87cf2c3472ff749fe7d2282b7106e8f1=1572947266,1573439674,1573532341,1573721165; JSESSIONID=C81EBB8AAB3A011BBA0C0DBA3930A070; Hm_lpvt_87cf2c3472ff749fe7d2282b7106e8f1=1573784071; username=2017114242"
            }
domain = "http://jwc.swjtu.edu.cn"

r = requests.get(url=assess_list_url, headers=headers)
with open('test.html', 'wb') as f:
    f.write(r.content)

soup = BeautifulSoup(r.content, 'lxml')
tr = soup.find('table', id='table3').find_all('tr')
assess_list = []
for j in tr[1:]:
    td = j.find_all('td')
    link = td[-1].find('a')
    if link:
        link = link.get('href')
        link = domain + link[2:]
        assess_list.append(link)

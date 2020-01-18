import datetime
import base64
import json

from bs4 import BeautifulSoup

from app.config import CAPTCHA_DISCERN_URL
from app.spider.spiderbase import SpiderBase, Session
from utils import log, getuser_agent


class ScsdLogin(SpiderBase):
    def __init__(self, ):
        self.post_url = "http://202.115.194.60"
        self.login_url = "http://202.115.194.60/default.aspx"
        self.captcha_url = "http://202.115.194.60/CheckCode.aspx"
        self.headers = {
            "User-Agent": getuser_agent(),
            "Referer": "http://202.115.194.60/default.aspx",
            "X-Requested-With": "XMLHttpRequest",
        }
        self.domain = "http://202.115.194.60/"
        self.__VIEWSTATEGENERATOR = ''
        self.__EVENTVALIDATION = ''
        self.__VIEWSTATE = ''
        self.__EVENTTARGET = ''
        self.__EVENTARGUMENT = ''
        self.__LASTFOCUS = ''
        self.is_login = False
        self.sid = ''

    def make_session(self):
        session = Session()
        session.headers = self.headers
        return session

    def get_captcha_and_cookie(self, session):
        r = session.get(self.captcha_url, headers=self.headers)
        # s = requests.get(self.login_url, headers=self.headers)
        # soup = BeautifulSoup(s.text, "lxml")
        # self.__VIEWSTATEGENERATOR = soup.find('input', id='__VIEWSTATEGENERATOR', attrs={'value': True}).get('value', '')
        # self.__VIEWSTATE = soup.find('input', id='__VIEWSTATE', attrs={'value': True}).get('value', '')
        # self.__EVENTVALIDATION = soup.find('input', id='__EVENTVALIDATION', attrs={'value': True}).get('value', '')
        #
        # self.__EVENTTARGET = soup.find('input', id='__EVENTTARGET', attrs={'value': True}).get('value', '')
        # self.__EVENTARGUMENT = soup.find('input', id='__EVENTARGUMENT', attrs={'value': True}).get('value', '')
        # self.__LASTFOCUS = soup.find('input', id='__LASTFOCUS', attrs={'value': True}).get('value', '')
        if r.status_code != 200:
            log("获取验证码时发生了一些错误")
            raise ValueError('没有获取到验证码')
        # 处理验证码图片,cookie并返回
        image_base64 = base64.b64encode(r.content).decode()
        cookie_str = json.dumps(dict(r.cookies))
        return image_base64, cookie_str

    def active_cookies(self, form):
        session = self.make_session()
        today = datetime.date.today()

        d_time1 = datetime.datetime.strptime(str(today) + '22:10:00', '%Y-%m-%d%H:%M:%S')
        d_time2 = datetime.datetime.strptime(str(today) + '23:59:59', '%Y-%m-%d%H:%M:%S')
        d_time3 = datetime.datetime.strptime(str(today) + '00:00:00', '%Y-%m-%d%H:%M:%S')
        d_time4 = datetime.datetime.strptime(str(today) + '07:30:00', '%Y-%m-%d%H:%M:%S')

        if d_time1 < datetime.datetime.now() < d_time2 or d_time3 < datetime.datetime.now() < d_time4:
            return False
        else:
            image_base64, cookies_str = self.get_captcha_and_cookie(session)
            data = {
                "image": image_base64,
            }
            r = session.post(url=CAPTCHA_DISCERN_URL, json=data)
            data = r.json()
            captcha_code = data["message"] if data["code"] == 0 else ''

            # captcha_code = form["code"]
            username = form["username"]
            password = form["password"]
            # cookies_str = form["cookies_str"]
            cookies = json.loads(cookies_str)
            for k, v in cookies.items():
                session.cookies.set(name=k, value=v)
            session = self.post_data(session, username, password, captcha_code)
            return session
        # return self.login_test(session)

    def post_data(self, session, username, password, captcha_code):
        try:
            s = session.get(self.login_url, headers=self.headers, allow_redirects=False)
            location = s.headers['Location']
            self.post_url += location
            self.domain += location.split('/', )[1]
        except Exception as e:
            log('****获取师大uri失败', e)
        data = {
            "tbUserName": username,
            "tbPassWord": password,
            "__VIEWSTATE": "/wEPDwUKLTY5MjYxMTQ3Mg9kFgICAw9kFggCAQ8PFgIeB1Zpc2libGVoZGQCAw8PFgIfAGdkZAIFDw9kFgIeB29uZm9jdXMFDnRoaXMuc2VsZWN0KCk7ZAIJDw9kFgQeBXZhbHVlZB8BBQ50aGlzLnNlbGVjdCgpO2RkGi4Vb72gX0UIFUcTAE6scZZ9X3+T4JrRe/pDtwMW9kU=",
            "__VIEWSTATEGENERATOR": "CA0B0334",
            "__EVENTVALIDATION": "/wEdAAUtAbsuhE8JD2uNChpmTBoghI6Xi65hwcQ8/QoQCF8JIZ/NcOJr6eLkhJ4xDLXjUJKFa3z02QmQnYFjj3wKxfjrop4oRunf14dz2Zt2+QKDENDihH3gMBj8KF0p73BiYV+weyqB0g9jkGjo/tdOhKiX",
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "btnLogin": '',
            "txtCode": captcha_code,
        }
        r = session.post(self.post_url, data)
        if "处理数据" in r.text:
            self.is_login = True
            log("四川师范", username, "****登录成功")
        else:
            log("****四川师范登录失败", username)
        soup = BeautifulSoup(r.text, 'lxml')
        self.sid = soup.find('form', id='form1').get('action')
        return session



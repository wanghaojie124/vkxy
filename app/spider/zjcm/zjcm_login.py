import datetime
import base64
import json
from bs4 import BeautifulSoup
from app.config import CAPTCHA_DISCERN_URL
from app.spider.spiderbase import SpiderBase, Session
from utils import log, getuser_agent


class ZjcmLogin(SpiderBase):
    def __init__(self):
        self.login_url = "http://xuanke.cuz.edu.cn/"
        self.captcha_url = "http://xuanke.cuz.edu.cn/CheckCode.aspx"
        self.headers = {
            "User-Agent": getuser_agent(),
            "X-Requested-With": "XMLHttpRequest",
        }
        self.is_login = False

    def make_session(self):
        session = Session()
        session.headers = self.headers
        return session

    def get_captcha_and_cookie(self, session):
        r = session.get(self.captcha_url, headers=self.headers)
        if r.status_code != 200:
            log("获取验证码时发生了一些错误")
            raise ValueError('没有获取到验证码')
        # 处理验证码图片,cookie并返回
        image_base64 = base64.b64encode(r.content).decode()
        cookie_str = json.dumps(dict(r.cookies))
        return image_base64, cookie_str

    def active_cookies(self, form):
        session = self.make_session()

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

    def post_data(self, session, username, password, captcha_code):
        data = {
            "txtUserName": username,
            "TextBox2": password,
            "__VIEWSTATE": "",
            "__VIEWSTATEGENERATOR": "",
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "RadioButtonList1": '学生',
            "txtSecretCode": captcha_code,
            "Button1": "登录"
        }
        resp = session.get(self.login_url)
        soup = BeautifulSoup(resp.text, "lxml")
        data["__VIEWSTATEGENERATOR"] = soup.find('input', id='__VIEWSTATEGENERATOR', attrs={'value': True}).get('value', '')
        data["__VIEWSTATE"] = soup.find('input', id='__VIEWSTATE', attrs={'value': True}).get('value', '')

        data["__EVENTTARGET"] = soup.find('input', id='__EVENTTARGET', attrs={'value': True}).get('value', '')
        data["__EVENTARGUMENT"] = soup.find('input', id='__EVENTARGUMENT', attrs={'value': True}).get('value', '')
        data["__LASTFOCUS"] = soup.find('input', id='__LASTFOCUS', attrs={'value': True}).get('value', '')
        r = session.post(self.login_url, data)
        if "欢迎您" in r.text:
            self.is_login = True
            log("浙江传媒", username, "****登录成功")
        else:
            log("****浙江传媒登录失败", username)
        return session

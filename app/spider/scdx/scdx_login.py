import base64
import json
import hashlib

import requests

from app.config import CAPTCHA_DISCERN_URL
from app.spider.spiderbase import SpiderBase, Session
from utils import log, getuser_agent


class ScdxLogin(SpiderBase):
    def __init__(self, ):
        self.post_url = "http://zhjw.scu.edu.cn/j_spring_security_check"
        # self.login_url = "http://202.115.194.60/default.aspx"
        self.captcha_url = "http://zhjw.scu.edu.cn/img/captcha.jpg"
        self.headers = {
            "User-Agent": getuser_agent(),
            "Origin": "http://zhjw.scu.edu.cn",
            "Referer": "http://zhjw.scu.edu.cn/login",
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
        m = hashlib.md5()
        m.update(password.encode("utf-8"))
        password = m.hexdigest()
        data = {
            "j_username": username,
            "j_password": password,
            "j_captcha": captcha_code,
        }
        r = session.post(self.post_url, data)
        if "教务系统首页" in r.text:
            self.is_login = True
            log(username, "****登录成功")
        else:
            log("****登录失败", username)
        return session



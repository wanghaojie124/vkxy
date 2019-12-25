import requests
import base64
import json

from app.config import CAPTCHA_DISCERN_URL
from app.spider.spiderbase import SpiderBase
from utils import log, getuser_agent


class XnjdLogin(SpiderBase):

    def __init__(self,):
        self.post_url = "http://jwc.swjtu.edu.cn/vatuu/UserLoginAction"
        self.captcha_url = "http://jwc.swjtu.edu.cn/vatuu/GetRandomNumberToJPEG"
        self.post_url1 = "http://jwc.swjtu.edu.cn/vatuu/UserLoadingAction"
        self.headers = {
            "User-Agent": getuser_agent(),
            "Referer": "http://jwc.swjtu.edu.cn/service/login.html?returnUrl=return",
            "X-Requested-With": "XMLHttpRequest"
        }
        self.test_url = "http://jwc.swjtu.edu.cn/vatuu/UserFramework"

    def make_session(self):
        session = requests.session()
        session.headers = self.headers
        # session.proxies = self.random_proxy
        return session

    def get_captcha_and_cookie(self,):
        r = requests.get(self.captcha_url, headers=self.headers)
        # r = requests.get(self.captcha_url, headers=self.headers, proxies=self.random_proxy)
        # s = requests.get('http://httpbin.org/get', headers=self.headers, proxies=self.random_proxy)
        # print(s.content)
        if r.status_code != 200:
            log("获取验证码时发生了一些错误")
            raise ValueError('没有获取到验证码')
        # 处理验证码图片,cookie并返回
        image_base64 = base64.b64encode(r.content).decode()
        cookie_str = json.dumps(dict(r.cookies))
        return image_base64, cookie_str

    def active_cookies(self, form):
        session = self.make_session()

        image_base64, cookies_str = self.get_captcha_and_cookie()
        data = {
            "image": image_base64,
        }
        r = requests.post(url=CAPTCHA_DISCERN_URL, json=data)
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
        data = {
            "username": username,
            "password": password,
            "url": "http://jwc.swjtu.edu.cn/index.html",
            "returnUrl": "return",
            "area": "",
            "ranstring": captcha_code,
        }
        r = session.post(self.post_url, data)
        log(r.content.decode())
        data1 = {
            # "url": "http://jwc.swjtu.edu.cn/vatuu/CourseAction?setAction=queryCourseList&selectTableType=ThisTerm",
            "returnUrl": "return",
            "loginMsg": "xxx"
        }
        r = session.post(self.post_url1, data=data1)

        # print(r.content.decode())
        return session

    def login_test(self, session):
        r = session.get(self.test_url)
        if "封未读消息" in r.content.decode():
            log("登陆成功")
            return True
        else:
            log("登录失败")
            return False




import requests
import base64
import json

from utils import log


class XnjdLogin:

    def __init__(self,):
        self.post_url = "http://jwc.swjtu.edu.cn/vatuu/UserLoginAction"
        self.captcha_url = "http://jwc.swjtu.edu.cn/vatuu/GetRandomNumberToJPEG"
        self.post_url1 = "http://jwc.swjtu.edu.cn/vatuu/UserLoadingAction"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "Referer": "http://jwc.swjtu.edu.cn/service/login.html?returnUrl=return",
            "X-Requested-With": "XMLHttpRequest"
        }
        self.test_url = "http://jwc.swjtu.edu.cn/vatuu/UserFramework"

    def make_session(self):
        session = requests.session()
        session.headers = self.headers
        return session

    def get_captcha_and_cookie(self,):
        r = requests.get(self.captcha_url, headers=self.headers)
        if r.status_code != 200:
            log("获取验证码时发生了一些错误")
            raise ValueError('没有获取到验证码')
        # 处理验证码图片,cookie并返回
        image_base64 = base64.b64encode(r.content).decode()
        cookie_str = json.dumps(dict(r.cookies))
        return image_base64, cookie_str

    def active_cookies(self, form):
        session = self.make_session()
        captcha_code = form["code"]
        username = form["username"]
        password = form["password"]
        cookies_str = form["cookies_str"]
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




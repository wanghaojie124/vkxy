from flask import request

from app.spider.scdx.scdx_assess import ScdxAssess
from app.spider.scdx.scdx_login import ScdxLogin
from app.spider.xnjd.xnjd_assess import XnjdAssess
from app.spider.xnjd.Xnjd_login import XnjdLogin
from app.models.user import User
from utils import log


class AssessController:

    def xnjd_assess(self, method):
        xnjd = XnjdLogin()
        if method == "GET":
            image_base64, cookies_str = xnjd.get_captcha_and_cookie()

            info = {
                'image_base64': image_base64,
                'cookies_str': cookies_str
            }
            return info
        if method == "POST":
            form = request.get_json()
            form['username'] = User.query.filter_by(id=form['uid']).first().username
            form['password'] = User.query.filter_by(id=form['uid']).first().password
            session = xnjd.active_cookies(form)

            if xnjd.login_test(session):
                assess = XnjdAssess()
                assess.main(form['uid'], session)

                data = {
                    'status': 200,
                    'msg': '评课已在后台进行'
                }
                return data
            else:
                log('*****用户名', form['username'], '在登录时发生了错误')
                return {
                    "status": 404,
                }

    def scdx_assess(self, method):
        scdx = ScdxLogin()
        if method == "GET":
            image_base64, cookies_str = scdx.get_captcha_and_cookie()

            info = {
                'image_base64': image_base64,
                'cookies_str': cookies_str
            }
            return info
        if method == "POST":
            form = request.get_json()
            form['username'] = User.query.filter_by(id=form['uid']).first().username
            form['password'] = User.query.filter_by(id=form['uid']).first().password
            session = scdx.active_cookies(form)

            if scdx.is_login:
                assess = ScdxAssess()
                assess.main(form['uid'], session)

                data = {
                    'status': 200,
                    'msg': '评课已在后台进行'
                }
                return data
            else:
                log('*****用户名', form['username'], '在登录时发生了错误')
                return {
                    "status": 404,
                }


    def main(self, college, method):
        if college == '西南交通大学':
            data = self.xnjd_assess(method)
            return data
        elif college == '四川大学':
            data = self.scdx_assess(method)
            return data
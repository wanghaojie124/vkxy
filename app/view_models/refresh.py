from flask import request
from app.models.user import User
from app.spider.scdx.scdx_login import ScdxLogin
from app.spider.scdx.scdx_spider import ScdxSpider
from app.spider.scsd.scsd_login import ScsdLogin
from app.spider.scsd.scsd_spider import ScsdSpider
from app.spider.xnjd.Xnjd_login import XnjdLogin
from app.spider.xnjd.Xnjd_spider import XnjdSpider
from utils import log


class RefreshController:

    def xnjd_refresh(self, method):
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
            i = 1
            while i < 4:
                session = xnjd.active_cookies(form)
                i += 1
                if xnjd.login_test(session):
                    break
            if xnjd.login_test(session):
                spider = XnjdSpider(session)
                spider.save_schedule(form['uid'])
                status = spider.save_score(form['uid'])
                spider.save_next_term_schedule(form['uid'])
                data = {
                    'status': 200,
                    'msg': '已更新数据'
                }
                if not status:
                    data['status'] = 404
                    data['msg'] = '获取成绩错误，可能是本学期未进行过考试或者需要进行课程评价'
                return data
            else:
                log('*****用户名', form['username'], '在登录时发生了错误')
                return {
                    "status": 404,
                }

    def scsd_refresh(self, method):
        scsd = ScsdLogin()

        if method == "GET":
            image_base64, cookies_str = scsd.get_captcha_and_cookie()

            info = {
                'image_base64': image_base64,
                'cookies_str': cookies_str,
            }
            return info

        if method == "POST":
            form = request.get_json()
            form['username'] = User.query.filter_by(id=form['uid']).first().username
            form['password'] = User.query.filter_by(id=form['uid']).first().password
            i = 1
            while i < 4:
                session = scsd.active_cookies(form)
                i += 1
                if scsd.is_login:
                    break
            if scsd.is_login:
                spider = ScsdSpider(session, scsd.domain, form['username'])
                spider.save_schedule(form['uid'])
                status = spider.save_score(form['uid'])
                spider.save_total_score(form['uid'])
                data = {
                    'status': 200,
                    'msg': '已更新数据'
                }
                if not status:
                    data['status'] = 404
                    data['msg'] = '获取成绩错误，可能是本学期未进行过考试或者需要进行课程评价'
                return data
            else:
                log('*****用户名', form['username'], '在登录时发生了错误')
                return {
                    "status": 404,
                }

    def scdx_refresh(self, method):
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
            i = 1
            while i < 4:
                session = scdx.active_cookies(form)
                i += 1
                if scdx.is_login:
                    break

            if scdx.is_login:
                spider = ScdxSpider(session, form['username'])
                spider.save_schedule(form['uid'])
                status = spider.save_score(form['uid'])
                spider.save_next_term_schedule(form['uid'])
                spider.save_total_score(form['uid'])
                data = {
                    'status': 200,
                    'msg': '已更新数据'
                }
                if not status:
                    data['status'] = 404
                    data['msg'] = '获取成绩错误，可能是本学期未进行过考试或者需要进行课程评价'
                return data
            else:
                log('*****用户名', form['username'], '在登录时发生了错误')
                return {
                    "status": 404,
                }

    def main(self, college, method):

        if college == '西南交通大学':
            data = self.xnjd_refresh(method)
            return data
        elif college == '四川大学':
            data = self.scdx_refresh(method)
            return data
        elif college == '四川师范大学':
            data = self.scsd_refresh(method)
            return data

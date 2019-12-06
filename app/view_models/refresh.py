from flask import request
from app.models.user import User
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
            session = xnjd.active_cookies(form)

            if xnjd.login_test(session):
                spider = XnjdSpider(session)
                spider.save_schedule(form['uid'])
                status = spider.save_score(form['uid'])
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
            session = scsd.active_cookies(form)
            if scsd.is_login:
                spider = ScsdSpider(session, scsd.domain, form['username'])
                spider.save_schedule(form['uid'])
                status = spider.save_score(form['uid'])
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
        elif college == '成都工业大学':
            pass
        elif college == '四川师范大学':
            data = self.scsd_refresh(method)
            return data

from flask import request
from app.models.user import User
from spider.Xnjd_login import XnjdLogin
from spider.Xnjd_spider import XnjdSpider
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
                spider.save_score(form['uid'])
                spider.save_schedule(form['uid'])

                return '已更新数据'
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

from flask import request
from app.models.user import User
from app.spider.scdx.scdx_login import ScdxLogin
from app.spider.scdx.scdx_spider import ScdxSpider
from app.spider.scsd.scsd_login import ScsdLogin
from app.spider.scsd.scsd_spider import ScsdSpider
from app.spider.xnjd.xnjd_login import XnjdLogin
from app.spider.xnjd.xnjd_spider import XnjdSpider
from app.spider.zjcm.zjcm_login import ZjcmLogin
from app.spider.zjcm.zjcm_spider import ZjcmSpider
from utils import log


class RefreshController:
    def refresh(self, method, model, spider):
        # if method == "GET":
        #     image_base64, cookies_str = model.get_captcha_and_cookie()
        #
        #     info = {
        #         'image_base64': image_base64,
        #         'cookies_str': cookies_str
        #     }
        #     return info

        if method == "POST":
            form = request.get_json()
            form['username'] = User.query.filter_by(id=form['uid']).first().username
            form['password'] = User.query.filter_by(id=form['uid']).first().password
            i = 1
            while i < 3:
                session = model.active_cookies(form)
                i += 1
                if model.is_login:
                    break
            if not session:
                return {
                    "status": 403,
                    'msg': '教务处已关闭'
                }

            if model.is_login:
                spider.session = session
                if isinstance(spider, ScsdSpider) or isinstance(spider, ScdxSpider) or isinstance(spider, ZjcmSpider):
                    spider.xh = form["username"]
                spider.save_schedule(form['uid'])
                status = spider.save_score(form['uid'])
                if isinstance(spider, ScsdSpider) or isinstance(spider, ScdxSpider):
                    spider.save_total_score(form['uid'])
                # if isinstance(spider, ScdxSpider) or isinstance(spider, XnjdSpider):
                #     spider.save_next_term_schedule(form['uid'])
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

    def xnjd_refresh(self, method):
        xnjd = XnjdLogin()
        spider = XnjdSpider(session=None)
        data = self.refresh(method, xnjd, spider)
        return data

    def scsd_refresh(self, method):
        scsd = ScsdLogin()
        # spider = ScsdSpider(session=None, domain=scsd.domain, username=None)
        # data = self.refresh(method, scsd, spider)
        # return data
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
            while i < 3:
                session = scsd.active_cookies(form)
                i += 1
                if scsd.is_login:
                    break

            if not session:
                return {
                    "status": 403,
                    'msg': '教务处已关闭'
                }

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
        spider = ScdxSpider(session=None, xh=None)
        data = self.refresh(method, scdx, spider)
        return data

    def zjcm_refresh(self, method):
        zjcm = ZjcmLogin()
        # spider = ZjcmSpider(session=None, username=None)
        # data = self.refresh(method, zjcm, spider)
        # return data
        if method == "POST":
            form = request.get_json()
            form['username'] = User.query.filter_by(id=form['uid']).first().username
            form['password'] = User.query.filter_by(id=form['uid']).first().password
            i = 1
            while i < 3:
                session = zjcm.active_cookies(form)
                i += 1
                if zjcm.is_login:
                    break

            if not session:
                return {
                    "status": 403,
                    'msg': '教务处已关闭'
                }

            if zjcm.is_login:
                spider = ZjcmSpider(session, form['username'])
                spider.save_schedule(form['uid'])
                status = spider.save_score(form['uid'])
                # spider.save_next_term_schedule(form['uid'])
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
        elif college == '浙江传媒学院':
            data = self.zjcm_refresh(method)
            return data

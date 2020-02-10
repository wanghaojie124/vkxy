from threading import Thread
from flask import request, current_app
from flask_login import login_user, current_user
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


class LoginController:
    # 异步处理数据，保存user姓名，学校，以及调用该学生学校的方法保存课表和成绩
    def save_async_db(self, app, form, uid, spider):
        with app.app_context():
            try:
                user = User()
                # 先调用schedule，确保xh与name不会为空
                spider.save_schedule(uid)
                spider.save_score(uid)
                if isinstance(spider, ScsdSpider) or isinstance(spider, ScdxSpider):
                    spider.save_total_score(uid)
                # if isinstance(spider, ScdxSpider) or isinstance(spider, XnjdSpider):
                #     spider.save_next_term_schedule(uid)
                # 保存用户姓名及学校
                user.save_name(form['username'], spider.name, spider.college)
                log(uid, "*****存储数据完毕")
            except Exception as e:
                log(uid, '*****异步存储数据发生了错误', e)

    # 异步存储数据入口函数
    def save_to_db(self, form, uid, spider):
        app = current_app._get_current_object()
        thr = Thread(target=self.save_async_db, args=[app, form, uid, spider])
        thr.start()
        log(uid, "开启新线程保存数据")

    def login(self, method, model, spider):
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
            session = model.active_cookies(form)

            # 进行是否登入教务系统判断
            if model.is_login:
                # 在登录进入教务系统后，进行如下操作
                # 实例化User，并保存入数据库
                user = User()
                user.save_to_db(form)
                # 将user数据传入login_user方便获取当前用户信息
                user = User.query.filter_by(username=form['username']).first()
                login_user(user)
                uid = current_user.id

                # 定义一个新的函数，开启新线程异步将输入存入数据库
                spider.session = session
                self.save_to_db(form, uid, spider)

                user = User.query.filter_by(username=form['username']).first()
                success_data = {
                    "username": user.username,
                    "name": user.name,
                    "uid": user.id,
                    "status": 200,
                }
                return success_data
            else:
                log('*****用户名', form['username'], '在登录时发生了错误')
                return {
                    "status": 404,
                }

    # 西南交大登录函数
    def xnjd_login(self, method):
        xnjd = XnjdLogin()
        spider = XnjdSpider(session=None)
        data = self.login(method, xnjd, spider)
        return data

    # TODO 川师不能进行函数提取，否则会登录失败
    def scsd_login(self, method):
        scsd = ScsdLogin()

        if method == "POST":
            form = request.get_json()
            session = scsd.active_cookies(form)

            # 进行是否登入教务系统判断
            if scsd.is_login:
                # 在登录进入教务系统后，进行如下操作
                # 实例化User，并保存入数据库
                user = User()
                user.save_to_db(form)
                # 将user数据传入login_user方便获取当前用户信息
                user = User.query.filter_by(username=form['username']).first()
                login_user(user)
                uid = current_user.id

                spider = ScsdSpider(session=None, domain=scsd.domain, username=form['username'])
                # 定义一个新的函数，开启新线程异步将输入存入数据库
                spider.session = session
                self.save_to_db(form, uid, spider)

                user = User.query.filter_by(username=form['username']).first()
                success_data = {
                    "username": user.username,
                    "name": user.name,
                    "uid": user.id,
                    "status": 200,
                }
                return success_data
            else:
                log('*****用户名', form['username'], '在登录时发生了错误')
                return {
                    "status": 404,
                }

        # spider = ScsdSpider(session=None, domain=scsd.domain, username=form['username'])
        # data = self.login(method, scsd, spider)
        # return data

    # 四川大学登录函数
    def scdx_login(self, method):
        scdx = ScdxLogin()
        form = request.get_json()
        spider = ScdxSpider(session=None, xh=form['username'])
        data = self.login(method, scdx, spider)
        return data

    # 浙江传媒学院
    def zjcm_login(self, method):
        zjcm = ZjcmLogin()
        form = request.get_json()
        spider = ZjcmSpider(session=None, username=form["username"])
        data = self.login(method, zjcm, spider)
        return data

    def main(self, college, method):
        if college == '西南交通大学':
            data = self.xnjd_login(method)
            return data
        elif college == '四川大学':
            data = self.scdx_login(method)
            return data
        elif college == '四川师范大学':
            data = self.scsd_login(method)
            return data
        elif college == '浙江传媒学院':
            data = self.zjcm_login(method)
            return data

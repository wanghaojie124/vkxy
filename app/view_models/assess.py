from flask import request

from app.spider.scdx.scdx_assess import ScdxAssess
from app.spider.scdx.scdx_login import ScdxLogin
from app.spider.xnjd.xnjd_assess import XnjdAssess
from app.spider.xnjd.xnjd_login import XnjdLogin
from app.models.user import User
from utils import log


class AssessController:

    def xnjd_assess(self, method):
        xnjd = XnjdLogin()
        if method == "GET":
            uid = request.args.get('uid', '')
            form = {
                'username': '',
                'password': ''
            }
            form['username'] = User.query.filter_by(id=uid).first().username
            form['password'] = User.query.filter_by(id=uid).first().password
            i = 1
            while i < 4:
                session = xnjd.active_cookies(form)
                i += 1
                if xnjd.login_test(session):
                    break
            if xnjd.login_test(session):
                assess = XnjdAssess()
                assess.get_course_list(session)
                data = {
                    'status': 200,
                    'msg': '查询成功',
                    'course_list': assess.course
                }
                return data

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
                assess = XnjdAssess()
                assess.main(form['uid'], session)

                data = {
                    'status': 200,
                    'msg': '评课已在后台进行',
                    'course_list': assess.course
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
            uid = request.args.get('uid', '')
            form = {
                'username': '',
                'password': ''
            }
            form['username'] = User.query.filter_by(id=uid).first().username
            form['password'] = User.query.filter_by(id=uid).first().password
            i = 1
            while i < 4:
                session = scdx.active_cookies(form)
                i += 1
                if scdx.is_login:
                    break
            if scdx.is_login:
                assess = ScdxAssess()
                assess.get_course_list(session)
                data = {
                    'status': 200,
                    'msg': '查询成功',
                    'course_list': assess.course
                }
                return data

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
                assess = ScdxAssess()
                assess.main(form['uid'], session, form['username'])

                data = {
                    'status': 200,
                    'msg': '评课已在后台进行',
                    'course_list': assess.course
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

import json
import requests
from flask import request
from app.models.base import db
from app.models.wx_user import WxUser
from utils import log, black_list


class WxUserViewModel:

    def __init__(self):
        self.xnjd = {
            'appid': 'wx3d24fe5cf403823a',
            'secret': '6c81d88a062fb6bcd7155bc16dd5acd8'
        }
        self.scsd = {
            'appid': 'wx5f40198c782e865b',
            'secret': '1343a83fa60222e6c927c7669822bb0d'
        }
        self.scdx = {
            'appid': 'wxae01f112939fbfe5',
            'secret': 'fe08d6eb833b2bce19968e9352f2a526'
        }

        self.zjcm = {
            'appid': 'wxae01f112939fbfe5',
            'secret': 'fe08d6eb833b2bce19968e9352f2a526'
        }

    def get_openid(self, college):
        resp = {'code': 200, 'msg': '操作成功', 'data': {}}
        req = request.values
        code = req['code'] if 'code' in req else ''
        if not code or len(code) < 1:
            resp['code'] = -1
            resp['msg'] = '需要code'
            log('获取个人信息时，无有效code')
            return resp

        url = "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code" % \
              (college['appid'], college['secret'], code)
        r = requests.get(url)
        res = json.loads(r.text)

        user = WxUser()
        user_data = {
            'nickname': req['nickName'],
            'gender': req['gender'],
            'avatar_url': req['avatarUrl'],
            'city': req['city'],
            'province': req['province'],
            'session_key': res['session_key'],
            'openid': res['openid'],
        }

        wx_user = WxUser.query.filter_by(openid=user_data['openid']).first()
        if wx_user:
            with db.auto_commit():
                wx_user.setattr(user_data)
        else:
            with db.auto_commit():
                user.setattr(user_data)
                db.session.add(user)
        exce = ['gender', 'session_key', 'city', 'province']
        user_info = black_list(user_data, exce)
        resp['data'] = user_info
        return resp

    def main(self, college):
        if college == '西南交通大学':
            data = self.get_openid(self.xnjd)
            return data
        elif college == '四川大学':
            data = self.get_openid(self.scdx)
            return data
        elif college == '四川师范大学':
            data = self.get_openid(self.scsd)
            return data
        elif college == '浙江传媒学院':
            data = self.get_openid(self.zjcm)
            return data

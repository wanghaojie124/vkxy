import json
import requests
from flask import request
from app.config import WECHAT_APPID, WECHAT_APPSECRET
from app.models.base import db
from app.models.wx_user import WxUser
from utils import log, black_list


class WxUserViewModel:

    def __init__(self):
        pass

    def get_openid(self):
        resp = {'code': 200, 'msg': '操作成功', 'data': {}}
        req = request.values
        code = req['code'] if 'code' in req else ''
        if not code or len(code) < 1:
            resp['code'] = -1
            resp['msg'] = '需要code'
            log('获取个人信息时，无有效code')
            return resp

        url = "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code" % \
              (WECHAT_APPID, WECHAT_APPSECRET, code)
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

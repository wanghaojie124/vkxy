from flask import request, jsonify
import json
from app.models.user_schedule import UserSchedule
from app.models.user_score import UserScore
from app.config import WECHAT_APPSECRET, WECHAT_APPID
import requests
from app.models.base import db
from app.web import web
from app.form.refresh import RefreshController
from app.models.wx_user import WxUser
from app.form.login import LoginController
from app.models.articles import Articles
from app.models.images import Images
from utils import log


@web.route('/login', methods=["GET", "POST"])
def login():
    controller = LoginController()
    if request.method == "GET":
        college = request.args.get('college', '')
        data = controller.main(college, request.method)
        return jsonify(data)
    if request.method == "POST":
        college = request.get_json().get('college', '')
        data = controller.main(college, request.method)
        return jsonify(data)


@web.route('/', methods=["GET", "POST"])
def index():
    return 'yoooooooooo'


@web.route("/scores", methods=["POST"])
def get_scores():
    # 返回json格式的个人成绩信息
    uid = request.get_json().get('uid', '')
    res_list = UserScore.query.filter_by(uid=uid).all()
    i = 0
    result = {}
    for res in res_list:
        res_dict = json.loads(res.serialize)
        res_dict.pop('id')
        res_dict.pop('uid')
        result[i] = res_dict
        i += 1
    return jsonify(result)


@web.route("/schedule", methods=["POST"])
def get_schedule():
    # 返回json格式的个人课表信息
    uid = request.get_json().get('uid', '')
    res_list = UserSchedule.query.filter_by(uid=uid).all()
    i = 0
    result = {}

    for res in res_list:
        res_dict = json.loads(res.serialize)
        res_dict.pop('id')
        res_dict.pop('uid')
        result[i] = res_dict
        i += 1
    return jsonify(result)


# 微信授权处理
@web.route("/user/getuserinfo", methods=["GET", "POST"])
def get_user_info():
    resp = {'code': 200, 'msg': '操作成功', 'data': {}}
    req = request.values
    code = req['code'] if 'code' in req else ''
    if not code or len(code) < 1:
        resp['code'] = -1
        resp['msg'] = '需要code'
        log('获取个人信息时，无有效code')
        return jsonify(resp)

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
    resp['data'] = user_data
    wx_user = WxUser.query.filter_by(openid=user_data['openid']).first()
    if wx_user:
        with db.auto_commit():
            wx_user.setattr(user_data)
    else:
        with db.auto_commit():
            user.setattr(user_data)
            db.session.add(user)

    return jsonify(resp)


@web.route("/refresh", methods=["GET", "POST"])
def refresh():
    controller = RefreshController()
    if request.method == "GET":
        college = request.args.get('college', '')
        data = controller.main(college, request.method)
        return jsonify(data)

    if request.method == "POST":
        college = request.get_json().get('college', '')
        data = controller.main(college, request.method)
        return jsonify(data)


@web.route("/articlelist", methods=["GET"])
def get_articles_info():
    college = request.args.get('college', '')
    articles = Articles.query.filter_by(college=college).all()
    if articles:
        i = 0
        result = {}

        for res in articles:
            res_dict = json.loads(res.serialize)
            result[i] = res_dict
            i += 1
        return jsonify(result)
    else:
        data = {
            'msg': '暂时还没有数据，请联系管理员添加',
            'status': 404
        }
        return jsonify(data)


@web.route("/imagelist", methods=["GET"])
def get_image_info():
    college = request.args.get('college', '')
    images = Images.query.filter_by(college=college).all()
    if images:
        i = 0
        result = {}

        for res in images:
            res_dict = json.loads(res.serialize)
            result[i] = res_dict
            i += 1
        return json.dumps(result)
    else:
        data = {
            'msg': '暂时还没有数据，请联系管理员添加',
            'status': 404
        }
        return jsonify(data)

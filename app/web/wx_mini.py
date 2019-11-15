import datetime
from flask import request, jsonify, render_template
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
from app.models.banner import Banner
from app.static.image.dirname import IMAGE_PATH
from app.form.assess import AssessController
from utils import log, white_list, black_list, get_week_day


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
    res_list = UserScore.query.filter_by(uid=uid).order_by(UserScore.xueqi.desc()).all()
    result = []
    for res in res_list:
        res_dict = res.to_dict()
        exce = ['id', 'uid', 'status']
        res_dict = black_list(res_dict, exce)
        result.append(res_dict)
    return jsonify(result)


@web.route("/schedule", methods=["POST"])
def get_schedule():
    # 返回json格式的个人课表信息
    uid = request.get_json().get('uid', '')
    college = request.get_json().get('college', '')
    if college == "西南交通大学":
        res_list = UserSchedule.query.filter_by(uid=uid).all()
        result = []
        for res in res_list:
            res_dict = res.to_dict()
            exce = ['id', 'uid', 'status']
            res_dict = black_list(res_dict, exce)
            # 课程名称处理，拆开为课程名称，上课周数，上课地点，老师
            for k, v in res_dict.items():
                if isinstance(v, str) and '\xa0' in v:
                    v = v.split('\xa0')[1:]
                    try:
                        v2 = v[1]
                        v0 = v[0].split('）', 1)[0] + '）'
                        v1 = v[0].split('）', 1)[1]
                        v3 = '（' + v0.split('（', 1)[1]
                        v0 = v0.split('（', 1)[0]
                        v = [v0, v1, v2, v3]
                        res_dict[k] = v
                    except Exception as e:
                        log('*****在处理课程名称时发生了错误', e)
                    else:
                        res_dict[k] = v
            result.append(res_dict)
        return jsonify(result)
    else:
        info = {
            'status': 404,
            'msg': '需要参数college'
        }
        return jsonify(info)


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
    return jsonify(resp)


# 刷新课程表以及成绩
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
    # 分页查找数据返回
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    college = request.args.get('college', '')
    article_type = request.args.get('type', '')
    if article_type:
        paginate = Articles.query.filter_by(college=college, type=article_type).order_by(Articles.weight.desc()).paginate(page, limit, error_out=False)
    else:
        paginate = Articles.query.filter_by(college=college).order_by(Articles.weight.desc()).paginate(page, limit, error_out=False)
    articles = paginate.items
    # TODO 这里要取得nginx代理的静态图片url，保存到image属性中返回
    if articles:
        data = []
        result = {
            'pages': paginate.pages
        }
        for res in articles:
            res_dict = res.to_dict()
            exce = ['college', 'id', 'status']
            res_dict = black_list(res_dict, exce)
            data.append(res_dict)
        result['data'] = data
        return jsonify(result)
    else:
        data = {
            'msg': '暂时还没有数据，请联系管理员添加',
            'status': 404
        }
        return jsonify(data)


@web.route("/bannerlist", methods=["GET"])
def get_image_info():
    college = request.args.get('college', '')
    images = Banner.query.filter_by(college=college, special=0).all()
    # TODO 这里要取得nginx代理的静态图片url，保存到image属性中返回

    if images:
        result = []
        for res in images:
            res_dict = res.to_dict()
            wonder = ['weight', 'mini', 'link', 'image']
            res_dict = white_list(res_dict, wonder)
            result.append(res_dict)
        return json.dumps(result)
    else:
        data = {
            'msg': '暂时还没有数据，请联系管理员添加',
            'status': 404
        }
        return jsonify(data)


@web.route("/top", methods=["GET"])
def get_top_news():
    college = request.args.get('college', '')
    if college == "西南交通大学":
        articles = Articles.query.filter_by(college=college, on_index=1).all()
        if articles:
            result = []
            for res in articles:
                res_dict = res.to_dict()
                result.append(res_dict)
            return jsonify(result)
        else:
            data = {
                'msg': '暂时还没有数据，请联系管理员添加',
                'status': 404
            }
            return jsonify(data)
    else:
        info = {
            'status': 404,
            'msg': '需要参数college或者college错误'
        }
        return jsonify(info)


@web.route("/special", methods=["GET"])
def get_special():
    college = request.args.get('college', '')
    images = Banner.query.filter_by(college=college, special=1).all()
    # TODO 这里要取得nginx代理的静态图片url，保存到image属性中返回
    if images:
        result = []
        for res in images:
            res_dict = res.to_dict()
            wonder = ['title', 'image', 'price', 'bargain_price', 'mini', 'link']
            res_dict = white_list(res_dict, wonder)
            result.append(res_dict)
        return json.dumps(result)
    else:
        data = {
            'msg': '暂时还没有数据，请联系管理员添加',
            'status': 404
        }
        return jsonify(data)


# 后台上传图片预备代码
@web.route("/test", methods=["GET", "POST"])
def test():
    if request.method == "GET":
        return render_template('404.html')
    if request.method == "POST":
        image = request.files['image']
        path = IMAGE_PATH + '\\'
        file_path = path + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
        image.save(file_path)
        return 'ok'


@web.route("/todayclass", methods=["POST"])
def get_today_class():
    # 返回json格式的个人成绩信息
    uid = request.get_json().get('uid', '')
    weekday = get_week_day(datetime.datetime.now())
    college = request.get_json().get('college', '')
    if college == "西南交通大学":
        res_list = UserSchedule.query.filter_by(uid=uid).all()
        result = []
        for res in res_list:
            res_dict = res.to_dict()
            wonder = ['jie', weekday]
            res_dict = white_list(res_dict, wonder)
            # 课程名称处理，拆开为课程名称，上课周数，上课地点，老师
            for k, v in res_dict.items():
                if isinstance(v, str) and '\xa0' in v:
                    v = v.split('\xa0')[1:]
                    try:
                        v2 = v[1]
                        v0 = v[0].split('）', 1)[0] + '）'
                        v1 = v[0].split('）', 1)[1]
                        v3 = '（' + v0.split('（', 1)[1]
                        v0 = v0.split('（', 1)[0]
                        v = [v0, v1, v2, v3]
                        res_dict[k] = v
                    except Exception as e:
                        log('*****在处理课程名称时发生了错误', e)
                    else:
                        res_dict[k] = v
            result.append(res_dict)
        return jsonify(result)
    else:
        info = {
            'status': 404,
            'msg': '需要参数college'
        }
        log("*****请求今日课表时缺少college参数")
        return jsonify(info)


@web.route("/assess", methods=["GET", "POST"])
def make_assess():
    controller = AssessController()
    if request.method == "GET":
        college = request.args.get('college', '')
        data = controller.main(college, request.method)
        return jsonify(data)

    if request.method == "POST":
        college = request.get_json().get('college', '')
        data = controller.main(college, request.method)
        return jsonify(data)

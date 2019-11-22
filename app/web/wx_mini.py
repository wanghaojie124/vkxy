from flask import request, jsonify, render_template

from app.config import IMAGE_DOMAIN
from app.models.user_score import UserScore
from app.web import web
from app.view_models.refresh import RefreshController
from app.view_models.login import LoginController
from app.models.articles import Articles
from app.models.banner import Banner
from app.view_models.assess import AssessController
from utils import log, white_list, black_list, get_week_day
from app.view_models.wx_user import WxUserViewModel
from app.view_models.schedule import ScheduleController
from app.view_models.articles import ArticleController


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
    request_week = request.get_json().get('request_week', '')
    controller = ScheduleController()
    resp = controller.main(college, uid, request_week)
    return jsonify(resp)


# 微信授权处理
@web.route("/user/getuserinfo", methods=["GET", "POST"])
def get_user_info():
    wx_user = WxUserViewModel()
    resp = wx_user.get_openid()
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
    # 分页查找数据返回
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    college = request.args.get('college', '')
    article_type = request.args.get('type', '')
    articles = ArticleController()
    resp = articles.get_mini_articles(article_type, college, page, limit)
    return jsonify(resp)


@web.route("/bannerlist", methods=["GET"])
def get_image_info():
    college = request.args.get('college', '')
    images = Banner.query.filter_by(college=college, special=0).all()
    if images:
        result = []
        for res in images:
            res_dict = res.to_dict()
            wonder = ['weight', 'mini', 'link', 'image']
            res_dict = white_list(res_dict, wonder)
            res_dict['image'] = IMAGE_DOMAIN + res_dict['image']
            result.append(res_dict)
        return jsonify(result)
    else:
        data = {
            'msg': '暂时还没有数据，请联系管理员添加',
            'status': 404
        }
        return jsonify(data)


# 公告栏
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


# 今日特价
@web.route("/special", methods=["GET"])
def get_special():
    college = request.args.get('college', '')
    images = Banner.query.filter_by(college=college, special=1).all()
    if images:
        result = []
        for res in images:
            res_dict = res.to_dict()
            wonder = ['title', 'image', 'price', 'bargain_price', 'mini', 'link']
            res_dict = white_list(res_dict, wonder)
            res_dict['image'] = IMAGE_DOMAIN + res_dict['image']
            result.append(res_dict)
        return jsonify(result)
    else:
        data = {
            'msg': '暂时还没有数据，请联系管理员添加',
            'status': 404
        }
        return jsonify(data)


# 今日课表
@web.route("/todayclass", methods=["POST"])
def get_today_class():
    # 返回json格式的个人成绩信息
    uid = request.get_json().get('uid', '')
    college = request.get_json().get('college', '')
    controller = ScheduleController()
    resp = controller.today_schedule_main(college, uid)
    return jsonify(resp)


# 一键评课
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

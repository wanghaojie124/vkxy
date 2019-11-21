import datetime
from flask import request, jsonify
from app.web import web
from app.models.base import db
from app.models.banner import Banner
from app.models.user import User
from flask_login import login_required, login_user
from app.models.administrators import Administrators
from app.static.image.dirname import IMAGE_PATH
from utils import black_list
from app.view_models.articles import ArticleController


@web.route("/vk/login", methods=["GET", "POST"])
def vk_login():
    if request.method == "GET":
        return 'This is api'
    if request.method == "POST":
        print(request.values)
        form = request.get_json()
        admin = Administrators.query.filter_by(username=form['username']).first()
        if form['username'] == admin.username and form['password'] == admin.password:
            login_user(admin)
            resp = {
                "code": 200,
                "message": "generate answer ok",
                "data": {
                    "username": "admin",
                    "token": "If necessary, this will be a token"
                }
            }
            return jsonify(resp)
        else:
            resp = {
                'code': "404",
                'msg': '口令或者用户名错误'
            }
            return jsonify(resp)


@web.route("/vk/articlelist", methods=["GET"])
@login_required
def get_articles():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    college = request.args.get('college', '')
    articles = ArticleController()
    resp = articles.get_vk_articles(college, page, limit)
    return jsonify(resp)


@web.route("/vk/addarticle", methods=["POST"])
@login_required
def add_articles():
    article = ArticleController()
    resp = article.save_article()
    return jsonify(resp)


@web.route("/vk/bannerlist", methods=["GET"])
@login_required
def get_images():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    college = request.args.get('college', '')
    if college:
        banners = Banner.query.filter_by(college=college).order_by(Banner.weight)\
            .paginate(page, limit, error_out=False)
    else:
        banners = Banner.query.filter_by().order_by(Banner.weight) \
            .paginate(page, limit, error_out=False)
    if banners:
        data = []
        result = {
            'pages': banners.pages,
            'total': banners.total
        }
        for res in banners.items:
            res_dict = res.to_dict()
            # res_dict['image'] = 'http://129.204.61.233:2000/images/' + res_dict['image']
            data.append(res_dict)
        result['data'] = data
        return jsonify(result)
    else:
        data = {
            'msg': '暂时还没有数据，请联系管理员添加',
            'status': 404
        }
        return jsonify(data)


@web.route("/vk/addbanner", methods=["POST"])
@login_required
def add_banners():
    banner = Banner()
    form = request.form
    banner_item = Banner.query.filter_by(title=form['title']).first()
    # TODO 这里要写文件保存到本地，将image替换为文件名 done
    image = request.files.get['image']
    path = IMAGE_PATH + '\\'
    if banner_item:
        file_name = banner_item.image
        file_path = path + file_name
        image.save(file_path)
        with db.auto_commit():
            banner_item.setattr(form)
            banner_item.image = file_name
        data = {
            'status': 200,
            'msg': '已更新数据'
        }
        return jsonify(data)
    else:
        file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
        file_path = path + file_name
        image.save(file_path)
        with db.auto_commit():
            banner.setattr(form)
            banner.image = file_name
            db.session.add(banner)
        data = {
            'status': 200,
            'msg': '已储存数据'
        }
        return jsonify(data)


@web.route("/vk/users", methods=["get"])
@login_required
def get_users():
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    college = request.args.get('college', '')
    if college:
        users = User.query.filter_by(college=college).order_by(User.id)\
            .paginate(page, limit, error_out=False)
    else:
        users = User.query.filter_by().order_by(User.id) \
            .paginate(page, limit, error_out=False)
    if users:
        data = []
        result = {
            'pages': users.pages,
            'total': users.total
        }
        for res in users.items:
            res_dict = res.to_dict()
            exce = ['status', 'password', 'college', 'openid']
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


@web.route("/vk/updatearticles", methods=["GET", "POST"])
@login_required
def update_article():
    article = ArticleController()
    resp = article.update()
    return jsonify(resp)


@web.route("/vk/updatebanners", methods=["GET", "POST"])
@login_required
def update_banner():
    form = request.form
    banner_item = Banner.query.get(form['id'])
    if request.method == "GET":
        if banner_item:
            res = banner_item.to_dict()
            # res['image'] = 'http://129.204.61.233:2000/images/' + res['image']
            return jsonify(res)
        else:
            data = {
                'status': 404,
                'msg': '没有找到该条数据'
            }
            return jsonify(data)
    if request.method == "POST":
        if form['status'] == 0:
            with db.auto_commit():
                banner_item.setattr(form)
        else:
            path = IMAGE_PATH + '\\'
            file_name = banner_item.image
            image = request.files.get('image', '')
            if image:
                file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
                file_path = path + file_name
                image.save(file_path)
            with db.auto_commit():
                banner_item.setattr(form)
                banner_item.image = file_name
            data = {
                'status': 200,
                'msg': '已更新数据'
            }
            return jsonify(data)

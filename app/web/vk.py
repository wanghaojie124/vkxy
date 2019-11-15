import json
from flask import request, jsonify
from app.web import web
from app.models.articles import Articles
from app.models.base import db
from app.models.banner import Banner
from app.models.user import User


@web.route("/vk/login/", methods=["GET", "POST"])
def vk_login():
    if request.method == "GET":
        return 'This is api'
    if request.method == "POST":
        if request.get_json().get('username', '') == 'admin' and request.get_json().get('password', '') == '123456':
            resp = {
                "code": 200,
                "message": "generate answer ok",
                "data": {
                    "answer": "Following will play the Chrismas song: Jingle Bells ...",
                    "audio": {
                        "contentType": "audio/mpeg",
                        "name": "Jingle Bells.mp3",
                        "url": "http://1.2.3.4/a/b/c.mp3"
                    }
                }
            }
            return jsonify(resp)
        else:
            return '口令或者用户名错误'


@web.route("/vk/articlelist", methods=["GET"])
def get_articles():
    articles = Articles.query.filter_by().all()
    # TODO 这里要取得nginx代理的静态图片url，保存到image属性中返回
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


@web.route("/vk/addarticle", methods=["POST"])
def add_articles():
    articles = Articles()
    form = request.get_json()
    article = Articles.query.filter_by(title=form['title']).first()
    # TODO 这里要写文件保存到本地，将image替换为文件名
    if article:
        with db.auto_commit():
            article.setattr(form)
        data = {
            'status': 200,
            'msg': '已更新数据'
        }
        return data
    else:
        with db.auto_commit():
            articles.setattr(form)
            db.session.add(articles)
        data = {
            'status': 200,
            'msg': '已储存数据'
        }
        return data


@web.route("/vk/bannerlist", methods=["GET"])
def get_images():
    images = Banner.query.filter_by().all()
    # TODO 这里要取得nginx代理的静态图片url，保存到image属性中返回
    if images:
        result = []
        for res in images:
            res_dict = res.to_dict()
            result.append(res_dict)
        return jsonify(result)
    else:
        data = {
            'msg': '暂时还没有数据，请联系管理员添加',
            'status': 404
        }
        return jsonify(data)


@web.route("/vk/addbanner", methods=["POST"])
def add_images():
    images = Banner()
    form = request.get_json()
    image = Banner.query.filter_by(title=form['title']).first()
    # TODO 这里要写文件保存到本地，将image替换为文件名
    if image:
        with db.auto_commit():
            image.setattr(form)
        data = {
            'status': 200,
            'msg': '已更新数据'
        }
        return data
    else:
        with db.auto_commit():
            images.setattr(form)
            db.session.add(images)
        data = {
            'status': 200,
            'msg': '已储存数据'
        }
        return data


@web.route("/vk/users", methods=["get"])
def get_users():
    users = User.query.filter_by(college='西南交通大学').all()
    if users:
        result = []
        for res in users:
            res_dict = res.to_dict()
            result.append(res_dict)
        return jsonify(result)
    else:
        data = {
            'msg': '暂时还没有数据，请联系管理员添加',
            'status': 404
        }
        return jsonify(data)


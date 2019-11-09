import json
from flask import request
from app.web import web
from app.models.articles import Articles
from app.models.base import db
from app.models.images import Images
from app.models.user import User


@web.route("/vk/login/", methods=["GET", "POST"])
def htdl():
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
            return json.dumps(resp)
        else:
            return '口令或者用户名错误'


@web.route("/vk/articlelist", methods=["GET"])
def get_articles():
    articles = Articles.query.filter_by().all()
    if articles:
        i = 0
        result = {}

        for res in articles:
            res_dict = json.loads(res.serialize)
            result[i] = res_dict
            i += 1
        return result
    else:
        return '暂时还没有数据，请添加'


@web.route("/vk/addarticle", methods=["POST"])
def add_articles():
    articles = Articles()
    form = request.get_json()
    article = Articles.query.filter_by(title=form['title']).first()
    if article:
        with db.auto_commit():
            article.setattr(form)
            print(article.serialize)
        return '已经保存啦'
    else:
        with db.auto_commit():
            articles.setattr(form)
            db.session.add(articles)
        return '已储存完毕'


@web.route("/vk/imagelist", methods=["GET"])
def get_images():
    images = Images.query.filter_by().all()
    if images:
        i = 0
        result = {}

        for res in images:
            res_dict = json.loads(res.serialize)
            result[i] = res_dict
            i += 1
        return result
    else:
        return '暂时还没有数据，请添加'


@web.route("/vk/addimage", methods=["POST"])
def add_images():
    images = Images()
    form = request.get_json()
    image = Images.query.filter_by(title=form['title']).first()
    if image:
        with db.auto_commit():
            image.setattr(form)
            print(image)
        return '已经保存啦'
    else:
        with db.auto_commit():
            images.setattr(form)
            db.session.add(images)
        return '已储存完毕'


@web.route("/vk/users", methods=["get"])
def get_users():
    users = User.query.filter_by(college='西南交通大学').all()
    if users:
        i = 0
        result = {}

        for res in users:
            res_dict = json.loads(res.serialize)
            result[i] = res_dict
            i += 1
        return result
    else:
        return '暂时还没有数据，请添加'

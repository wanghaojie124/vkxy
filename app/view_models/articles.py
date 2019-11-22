import datetime

from flask import request

from app.config import IMAGE_DOMAIN
from app.models.articles import Articles
from app.models.base import db
from app.static.image.dirname import IMAGE_PATH
from utils import black_list


class ArticleController:
    def get_mini_articles(self, article_type, college, page, limit):
        if article_type:
            paginate = Articles.query.filter_by(college=college, type=article_type) \
                .order_by(Articles.weight.desc()).paginate(page, limit, error_out=False)
        else:
            paginate = Articles.query.filter_by(college=college) \
                .order_by(Articles.weight.desc()).paginate(page, limit, error_out=False)
        articles = paginate.items
        if articles:
            data = []
            result = {
                'pages': paginate.pages,
            }
            for res in articles:
                res_dict = res.to_dict()
                exce = ['college', 'id', 'status']
                res_dict['image'] = IMAGE_DOMAIN + res_dict['image']
                res_dict = black_list(res_dict, exce)
                data.append(res_dict)
            result['data'] = data
            return result
        else:
            data = {
                'msg': '暂时还没有数据，请联系管理员添加',
                'status': 404
            }
            return data

    def get_vk_articles(self, college, page, limit):
        if college:
            articles = Articles.query.filter_by(college=college).order_by(Articles.weight.desc()) \
                .paginate(page, limit, error_out=False)
        else:
            articles = Articles.query.filter_by().order_by(Articles.weight.desc()) \
                .paginate(page, limit, error_out=False)

        if articles:
            data = []
            result = {
                'pages': articles.pages,
                'total': articles.total,
            }
            for res in articles.items:
                res_dict = res.to_dict()
                res_dict['image'] = IMAGE_DOMAIN + res_dict['image']
                data.append(res_dict)
            result['data'] = data
            return result
        else:
            data = {
                'msg': '暂时还没有数据，请联系管理员添加',
                'status': 404
            }
            return data

    def save_article(self):
        articles = Articles()
        form = request.form
        article = Articles.query.filter_by(title=form['title']).first()
        image = request.files['image']
        path = IMAGE_PATH + '/'
        if article:
            file_name = article.image
            file_path = path + file_name
            image.save(file_path)
            with db.auto_commit():
                article.setattr(form)
                article.image = file_name
            data = {
                'status': 200,
                'msg': '已更新数据'
            }
            return data
        else:
            file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
            file_path = path + file_name
            image.save(file_path)
            with db.auto_commit():
                articles.setattr(form)
                articles.image = file_name
                db.session.add(articles)
            data = {
                'status': 200,
                'msg': '已储存数据'
            }
            return data

    def update(self):
        form = request.form
        article_item = Articles.query.get(form['id'])
        if request.method == "GET":
            if article_item:
                res = article_item.to_dict()
                res['image'] = IMAGE_DOMAIN + res['image']
                return res
            else:
                data = {
                    'status': 404,
                    'msg': '没有找到该条数据'
                }
                return data
        if request.method == "POST":
            if form['status'] == 0:
                with db.auto_commit():
                    article_item.setattr(form)
            else:
                path = IMAGE_PATH + '/'
                file_name = article_item.image
                image = request.files['image']
                if image:
                    file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
                    file_path = path + file_name
                    image.save(file_path)
                with db.auto_commit():
                    article_item.setattr(form)
                    article_item.image = file_name
                data = {
                    'status': 200,
                    'msg': '已更新数据'
                }
                return data



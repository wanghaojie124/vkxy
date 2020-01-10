from flask import Blueprint, render_template, current_app, request
from app import cache
web = Blueprint('web', __name__)


@web.app_errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


def cache_with_param(timeout=None, key_prefix='view/%s', unless=None):
    """
    直接封装 cache.cached，使用起来更简单
    """
    def key_prefix_func():
        with current_app.app_context():
            if '%s' in key_prefix:
                cache_key = key_prefix % request.url
            else:
                cache_key = key_prefix
        return cache_key
    return cache.cached(timeout=timeout, key_prefix=key_prefix_func, unless=unless)


from app.web import wx_mini, vk

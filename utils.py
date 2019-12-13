import base64
import datetime
import time
from decimal import Decimal


def log(*args, **kwargs):
    format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('logs/log.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


def get_base64(image_path):
    try:
        with open(image_path, 'rb') as f:
            img = base64.b64encode(f.read()).decode()
            f.close()
        return img
    except Exception as e:
        log('*****读取图片时发生了错误', e)


# 实现字典的白名单效果，传入原始dict以及所需要的key列表，返回处理后的新dict
def white_list(obj, list):
    res = {}
    for k, v in obj.items():
        if k in list:
            res[k] = v
        else:
            pass
    return res


# 黑名单
def black_list(obj, list):
    res = {}
    for k, v in obj.items():
        if k in list:
            pass
        else:
            res[k] = v
    return res


def get_week_day(date):
    week_day_dict = {
        0: 'Mon',
        1: 'Tues',
        2: 'Wen',
        3: 'Thur',
        4: 'Fri',
        5: 'Sat',
        6: 'Sun',
    }
    day = date.weekday()
    return week_day_dict[day]


# print((datetime.datetime.now() - datetime.timedelta(days= 4)).strftime('%a'))
def default(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Object of type '%s' is not JSON serializable" % type(obj).__name__)


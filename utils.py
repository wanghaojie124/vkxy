import base64
import datetime
import random
import time
from qiniu import Auth, put_file, etag
import math
from app.config import QINIU_AK, QINIU_SK


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


# 根据日期获得自定义星期简称
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

# print((datetime.datetime.now() - datetime.timedelta(days= 4)).strftime('%a')).


# 根据起止周日期和指定日期获得当前周数,
def get_current_week(start_date, search_date):
    try:
        start_date = time.strptime(start_date, '%Y-%m-%d')
        search_date = time.strptime(search_date, '%Y-%m-%d')
        start_date_timestamp = int(time.mktime(start_date))
        search_date_timestamp = int(time.mktime(search_date))
        week = search_date_timestamp-start_date_timestamp
        week = week / 3600 / 24 / 7
        week = math.ceil(week)
        return week
    except Exception as ex:
        pass


# 根据当前日期、起止周日期和指定周，获取当前日期距指定周周数
def get_need_week(start_date, request_week):
    start_date1 = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    year = start_date1.year

    fir_day = datetime.datetime(year, 1, 1)
    request_week = request_week if request_week else 1
    search_date = 7 * int(request_week) + int(start_date1.strftime('%j')) - 7
    zone = datetime.timedelta(days=search_date)
    search_date = datetime.datetime.strftime(fir_day + zone, '%Y-%m-%d')

    current_date = datetime.datetime.now()
    search_date = datetime.datetime.strptime(search_date, '%Y-%m-%d')
    days = (current_date-search_date).days
    return math.ceil(days/7)


# 返回一个随机的请求头 headers
def getuser_agent():
    user_agent_list = [ \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]
    UserAgent = random.choice(user_agent_list)
    return UserAgent


def upload_qiniu(path, file_name):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = QINIU_AK
    secret_key = QINIU_SK
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'vkcampus'
    # 上传后保存的文件名
    key = 'images/' + file_name
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    # 要上传文件的本地路径
    localfile = path + file_name
    ret, info = put_file(token, key, localfile)
    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)


def func_time(f):
    """
    简单记录执行时间
    :param f:
    :return:
    """

    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print(f.__name__, 'took', end - start, 'seconds')
        return result

    return wrapper



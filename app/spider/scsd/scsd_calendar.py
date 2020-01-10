import time

from pyquery import PyQuery as pq

from app.spider.spiderbase import Session
from utils import getuser_agent
import re


def date_to_timestamp(date, format_string="%Y-%m-%d"):
    time_array = time.strptime(date, format_string)
    time_stamp = int(time.mktime(time_array))
    return time_stamp


def get_scsd_calendar():
    url = "http://jwc.sicnu.edu.cn/InfoService/calender.html"
    headers = {
        "User-Agent": getuser_agent(),
        "Referer": "http://jwc.swjtu.edu.cn/service/login.html?returnUrl=return",
        "X-Requested-With": "XMLHttpRequest"
    }
    session = Session()
    r = session.get(url, headers=headers).content.decode()
    page = pq(r)
    # 第一学期解析
    res = page('td.style8')
    day = pq(res[0]).text()
    day1 = re.findall(r'\d+', day)

    res = page('td.style9')
    month = pq(res[0]).text()
    month1 = re.findall(r'\d+', month)

    res = page('font.font7')
    fonts = pq(res)
    term = fonts[0]
    term = pq(term).text()
    term1 = term.split('-')[0]
    term2 = term.split('-')[1]

    total_weeks1 = fonts[1]
    total_weeks1 = pq(total_weeks1).text()
    total_weeks2 = fonts[2]
    total_weeks2 = pq(total_weeks2).text()

    tables = page('table')
    table2 = pq(pq(tables)[-1])
    res = table2('td.style8')
    day = pq(res[0]).text()
    day2 = re.findall(r'\d+', day)

    res = table2('td.style15')
    month = pq(res[0]).text()
    month2 = re.findall(r'\d+', month)

    scsd_begin_date1 = '-'.join(month1+day1)
    scsd_begin_date1 = term1 + '-' + scsd_begin_date1
    scsd_begin_date2 = '-'.join(month2+day2)
    scsd_begin_date2 = term2 + '-' + scsd_begin_date2

    scsd_begin_date1_stamp = date_to_timestamp(scsd_begin_date1)
    scsd_begin_date2_stamp = date_to_timestamp(scsd_begin_date2)
    current_time = int(time.time())

    if current_time > scsd_begin_date1_stamp and current_time < scsd_begin_date2_stamp:
        scsd_begin_date = scsd_begin_date1
        total_weeks = total_weeks1
        return scsd_begin_date, total_weeks
    elif current_time > scsd_begin_date2_stamp:
        scsd_begin_date = scsd_begin_date2
        total_weeks = total_weeks2
        return scsd_begin_date, total_weeks


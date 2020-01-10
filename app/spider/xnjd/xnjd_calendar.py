# 获取西南交通大学校历
import json
import time
from app.spider.spiderbase import Session
from utils import getuser_agent


class XnjdCalendar:
    term2 = ''
    def date_to_timestamp(self, date, format_string="%Y-%m-%d %H:%M:%S"):
        time_array = time.strptime(date, format_string)
        time_stamp = int(time.mktime(time_array))
        return time_stamp

    def get_xnjd_calendar(self):
        headers = {
            "User-Agent": getuser_agent(),
            "Referer": "http://jwc.swjtu.edu.cn/service/login.html?returnUrl=return",
            "X-Requested-With": "XMLHttpRequest"
        }

        url = 'http://jwc.swjtu.edu.cn/vatuu/SchoolDate?date=new%20Date()'
        data = {
            'date': 'new Date()'
        }
        session = Session()
        r = session.post(url, headers, data)
        date = json.loads(r.text)
        date = date['dateJson']
        xnjd_begin_date1 = ''
        xnjd_begin_date2 = ''
        total_weeks1 = '22'
        total_weeks2 = '23'
        for i in date:
            for k, v in i.items():
                if "第1学期" in v:
                    xnjd_begin_date1 = i['beginDate']
                else:
                    xnjd_begin_date2 = i['beginDate']

        xnjd_begin_date1 = xnjd_begin_date1.split('.')[0]
        xnjd_begin_date2 = xnjd_begin_date2.split('.')[0]

        xnjd_begin_date1_stamp = self.date_to_timestamp(xnjd_begin_date1)
        xnjd_begin_date2_stamp = self.date_to_timestamp(xnjd_begin_date2)
        current_time = int(time.time())
        self.term2 = xnjd_begin_date2.split(' ')[0]

        if current_time > xnjd_begin_date1_stamp and current_time < xnjd_begin_date2_stamp:
            xnjd_begin_date = xnjd_begin_date1.split(' ')[0]
            total_weeks = total_weeks1
            return xnjd_begin_date, total_weeks
        elif current_time > xnjd_begin_date2_stamp:
            xnjd_begin_date = xnjd_begin_date2.split(' ')[0]
            total_weeks = total_weeks2
            return xnjd_begin_date, total_weeks

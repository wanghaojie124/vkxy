import time
from datetime import datetime
import requests
from utils import getuser_agent


def date_to_timestamp(date, format_string="%Y-%m-%d %H:%M:%S"):
    time_array = time.strptime(date, format_string)
    time_stamp = int(time.mktime(time_array))
    return time_stamp


def get_scdx_calendar():
    year = datetime.now().strftime('%Y')
    month = datetime.now().strftime('%m')
    if int(month) > 8:
        url = "http://jwc.scu.edu.cn/scdx/xl{}.html".format(year)
    else:
        url = "http://jwc.scu.edu.cn/scdx/xl{}.html".format(str(int(year) - 1))
    headers = {
        "User-Agent": getuser_agent(),
        "Referer": "http://jwc.scu.edu.cn/article/206/206_1.htm",
        "Host": "jwc.scu.edu.cn"
    }
    r = requests.get(url, headers=headers)
    # TODO 延迟加载


SCDX_BEGIN_DATE = "2019-09-01"
SCDX_TOTAL_WEEKS = 20

SCDX_TERM2 = "2020-02-23"

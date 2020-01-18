import time


def date_to_timestamp(date, format_string="%Y-%m-%d %H:%M:%S"):
    time_array = time.strptime(date, format_string)
    time_stamp = int(time.mktime(time_array))
    return time_stamp


ZJCM_BEGIN_DATE = "2019-09-17"
ZJCM_TOTAL_WEEKS = 20

ZJCM_TERM2 = "2020-02-25"

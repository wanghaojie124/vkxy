from datetime import datetime
from app.models.user_schedule import UserSchedule
from utils import log, black_list, white_list, get_week_day
import re
from utils import get_current_week
from app.config import XNJD_TERM, XNJD_TOTAL_WEEK


class ScheduleController:

    def get_course_info(self, res):
        for k, v in res.items():
            if isinstance(v, list):
                week_str = v[1]
                if '单' in week_str:
                    s = re.findall(r'\d+', week_str)
                    weeks = range(int(s[0]), int(s[1]) + 1)
                    week_list = []
                    for i in weeks:
                        if (i % 2) != 0:
                            week_list.append(str(i))
                    v.append(week_list)
                elif '双' in week_str:
                    s = re.findall(r'\d+', week_str)
                    weeks = range(int(s[0]), int(s[1]) + 1)
                    week_list = []
                    for i in weeks:
                        if (i % 2) == 0:
                            week_list.append(str(i))
                    v.append(week_list)
                elif '-' in week_str:
                    s = re.findall(r'\d+', week_str)
                    weeks = range(int(s[0]), int(s[1]) + 1)
                    week_list = []
                    for i in weeks:
                        week_list.append(str(i))
                    v.append(week_list)
                elif ',' in week_str or '，' in week_str:
                    s = re.findall(r'\d+', week_str)
                    v.append(s)
                res[k] = v
        return res

    @staticmethod
    def get_request_schedule(res, request_week):
        pop_list = []
        for k, v in res.items():
            if isinstance(v, list):
                if str(request_week) not in v[4]:
                    pop_list.append(k)
        for i in pop_list:
            res.pop(i)
        return res

    def xnjd_schedule(self, uid, request_week):
        res_list = UserSchedule.query.filter_by(uid=uid).all()
        result = []
        current_week = get_current_week(XNJD_TERM, datetime.now().strftime('%Y-%m-%d'))
        for res in res_list:
            res_dict = res.to_dict()
            exce = ['id', 'uid', 'status']
            res_dict = black_list(res_dict, exce)
            # 课程名称处理，拆开为课程名称，上课周数，上课地点，老师
            for k, v in res_dict.items():
                if isinstance(v, str) and '\xa0' in v:
                    v = v.split('\xa0')[1:]
                    try:
                        v2 = v[1]
                        v0 = v[0].split('）', 1)[0] + '）'
                        v1 = v[0].split('）', 1)[1]
                        v3 = '（' + v0.split('（', 1)[1]
                        v0 = v0.split('（', 1)[0]
                        v = [v0, v1, v2, v3]
                        res_dict[k] = v
                    except Exception as e:
                        log('*****在处理课程名称时发生了错误', e)
                    else:
                        res_dict[k] = v
            res_dict = self.get_course_info(res_dict)
            if request_week:
                res_dict = self.get_request_schedule(res_dict, request_week)
            else:
                res_dict = self.get_request_schedule(res_dict, current_week)
            res_dict['current_week'] = current_week
            res_dict['total_weeks'] = XNJD_TOTAL_WEEK
            result.append(res_dict)
        return result

    def xnjd_today_schedule(self, uid):
        res_list = UserSchedule.query.filter_by(uid=uid).all()
        result = []
        for res in res_list:
            res_dict = res.to_dict()
            weekday = get_week_day(datetime.now())
            wonder = ['jie', weekday]
            res_dict = white_list(res_dict, wonder)
            # 课程名称处理，拆开为课程名称，上课周数，上课地点，老师
            for k, v in res_dict.items():
                if isinstance(v, str) and '\xa0' in v:
                    v = v.split('\xa0')[1:]
                    try:
                        v2 = v[1]
                        v0 = v[0].split('）', 1)[0] + '）'
                        v1 = v[0].split('）', 1)[1]
                        v3 = '（' + v0.split('（', 1)[1]
                        v0 = v0.split('（', 1)[0]
                        v = [v0, v1, v2, v3]
                        res_dict[k] = v
                    except Exception as e:
                        log('*****在处理课程名称时发生了错误', e)
                    else:
                        res_dict[k] = v
            current_week = get_current_week(XNJD_TERM, datetime.now().strftime('%Y-%m-%d'))
            res_dict = self.get_course_info(res_dict)
            res_dict = self.get_request_schedule(res_dict, current_week)
            result.append(res_dict)
        return result

    def main(self, college, uid, request_week):
        if college == '西南交通大学':
            data = self.xnjd_schedule(uid, request_week)
            return data
        elif college == '成都工业大学':
            pass
        else:
            info = {
                'status': 404,
                'msg': '需要参数college'
            }
            return info

    def today_schedule_main(self, college, uid):
        if college == '西南交通大学':
            data = self.xnjd_today_schedule(uid)
            return data
        elif college == '成都工业大学':
            pass
        else:
            info = {
                'status': 404,
                'msg': '需要参数college'
            }
            return info
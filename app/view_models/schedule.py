from datetime import datetime
from app.models.user_schedule import UserSchedule
from app.spider.scsd.scsd_calendar import get_scsd_calendar
from app.spider.xnjd.xnjd_calendar import get_xnjd_calendar
from utils import log, black_list, white_list, get_week_day
import re
from utils import get_current_week


class ScheduleController:

    def get_xnjd_course_info(self, res):
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

    def get_scsd_course_info(self, ex):
        for k, v in ex.items():
            if isinstance(v, str) and ';' in v:
                res = v.split(';')
                new_course_list = []
                for res_item in res:
                    result = res_item.split('\n')
                    result = [x.strip() for x in result if x.strip() != '']
                    teacher = result[1].split('[')[0]
                    address = result[1].split('[')[2]
                    weeks = re.findall(r'[(](.*?)[)]', result[1])[-1]
                    result[1] = weeks
                    result.append(address)
                    result.append(teacher)
                    new_course_list.append(result)
                ex[k] = new_course_list
            if isinstance(v, str) and '\n' in v and ';' not in v:
                res = v.split('\n')
                if '[' in res[1]:
                    teacher = res[1].split('[')[0]
                if '[' in res[2]:
                    address = res[2].split('[')[0]
                    weeks = res[2].split(']')[1]
                    weeks = re.findall(r'[(](.*?)[)]', weeks)[0]
                    # weeks = weeks.split('(')
                    res[1] = weeks
                    res[2] = address
                    res.append(teacher)
                ex[k] = res
        for k, v in ex.items():
            if isinstance(v, list):
                for item in v:
                    if isinstance(item, list):
                        week_str = item[1]
                        if '*' in item[0]:
                            s = re.findall(r'\d+', week_str)
                            weeks = range(int(s[0]), int(s[1]) + 1)
                            week_list = []
                            for i in weeks:
                                if (i % 2) != 0:
                                    week_list.append(str(i))
                            item.append(week_list)
                        elif '**' in item[0]:
                            s = re.findall(r'\d+', week_str)
                            weeks = range(int(s[0]), int(s[1]) + 1)
                            week_list = []
                            for i in weeks:
                                if (i % 2) == 0:
                                    week_list.append(str(i))
                            item.append(week_list)
                        elif '-' in week_str:
                            s = re.findall(r'\d+', week_str)
                            weeks = range(int(s[0]), int(s[1]) + 1)
                            week_list = []
                            for i in weeks:
                                week_list.append(str(i))
                            item.append(week_list)
                        elif ',' in week_str or '，' in week_str:
                            s = re.findall(r'\d+', week_str)
                            item.append(s)
                            ex[k] = item
                    elif not isinstance(item, list) and not isinstance(v[-1], list):
                        week_str = v[1]
                        if '*' in v[0] and '**' not in v[0]:
                            s = re.findall(r'\d+', week_str)
                            weeks = range(int(s[0]), int(s[1]) + 1)
                            week_list = []
                            for i in weeks:
                                if (i % 2) != 0:
                                    week_list.append(str(i))
                            v.append(week_list)
                        elif '**' in v[0]:
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
                            ex[k] = v
        return ex

    @staticmethod
    def get_request_schedule(res, request_week):
        pop_list = []
        for k, v in res.items():
            new_course = []
            if isinstance(v, list):
                if isinstance(v[0], list):
                    for item in v:
                        if str(request_week) in item[-1]:
                            new_course = item
                    res[k] = new_course
                else:
                    if str(request_week) not in v[-1]:
                        pop_list.append(k)
        for i in pop_list:
            res.pop(i)

        return res

    def xnjd_schedule(self, uid, request_week):
        res_list = UserSchedule.query.filter_by(uid=uid).all()
        result = []
        xnjd_begin_date, total_weeks = get_xnjd_calendar()
        current_week = get_current_week(xnjd_begin_date, datetime.now().strftime('%Y-%m-%d'))
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
            res_dict = self.get_xnjd_course_info(res_dict)
            if request_week:
                res_dict = self.get_request_schedule(res_dict, request_week)
            else:
                res_dict = self.get_request_schedule(res_dict, current_week)
            res_dict['current_week'] = current_week
            res_dict['total_weeks'] = total_weeks
            result.append(res_dict)
        return result

    def xnjd_today_schedule(self, uid):
        res_list = UserSchedule.query.filter_by(uid=uid).all()
        xnjd_begin_date, total_weeks = get_xnjd_calendar()
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
            current_week = get_current_week(xnjd_begin_date, datetime.now().strftime('%Y-%m-%d'))
            res_dict = self.get_xnjd_course_info(res_dict)
            res_dict = self.get_request_schedule(res_dict, current_week)
            result.append(res_dict)
        return result

    def scsd_schedule(self, uid, request_week):
        res_list = UserSchedule.query.filter_by(uid=uid).all()
        result = []
        scsd_begin_date, total_weeks = get_scsd_calendar()
        current_week = get_current_week(scsd_begin_date, datetime.now().strftime('%Y-%m-%d'))
        for res in res_list:
            res_dict = res.to_dict()
            exce = ['id', 'uid', 'status']
            res_dict = black_list(res_dict, exce)
            res_dict = self.get_scsd_course_info(res_dict)
            if request_week:
                res_dict = self.get_request_schedule(res_dict, request_week)
            else:
                res_dict = self.get_request_schedule(res_dict, current_week)
            res_dict['current_week'] = current_week
            res_dict['total_weeks'] = total_weeks
            result.append(res_dict)
        return result

    def scsd_today_schedule(self, uid):
        res_list = UserSchedule.query.filter_by(uid=uid).all()
        scsd_begin_date, total_weeks = get_scsd_calendar()
        result = []
        for res in res_list:
            res_dict = res.to_dict()
            weekday = get_week_day(datetime.now())
            wonder = ['jie', weekday]
            res_dict = white_list(res_dict, wonder)
            res_dict = self.get_scsd_course_info(res_dict)
            current_week = get_current_week(scsd_begin_date, datetime.now().strftime('%Y-%m-%d'))
            res_dict = self.get_request_schedule(res_dict, current_week)
            result.append(res_dict)
        return result

    def main(self, college, uid, request_week):
        if college == '西南交通大学':
            data = self.xnjd_schedule(uid, request_week)
            return data
        elif college == '四川师范大学':
            data = self.scsd_schedule(uid, request_week)
            return data
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
        elif college == '四川师范大学':
            data = self.scsd_today_schedule(uid)
            return data
        else:
            info = {
                'status': 404,
                'msg': '需要参数college'
            }
            return info
from datetime import datetime
from app.spider.scdx.scdx_calendar import SCDX_BEGIN_DATE, SCDX_TOTAL_WEEKS
from app.models.scdx_schedule import ScdxSchedule
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
                    weeks = re.findall(r'[(](.*?)[)]', result[1])[0]
                    result[1] = weeks
                    result.append(address)
                    result.append(teacher)
                    new_course_list.append(result)
                ex[k] = new_course_list
            elif isinstance(v, str) and '\n' in v and v.count('\n') > 3:
                if v.count('\n') < 5 and v.count('\n') > 2:
                    res = v.split('\n')
                    new_course_list = []
                    course = res[0]
                    teacher = ''
                    for i in res[1:]:
                        address = ''
                        weeks = ''
                        if '-' in i and '[' not in i:
                            address = i.split('(')[0]
                            weeks = re.findall(r'[(](.*?)[)]', i)[-1]
                        elif '[' in i:
                            teacher = i.split('[')[0]
                        new_course = [course, weeks, address, teacher]
                        new_course_list.append(new_course)
                    ex[k] = new_course_list

                if v.count('\n') == 5:
                    if ')\n' in v:
                        res = v.split(')\n')
                        res[0] = res[0] + ')'
                        new_course_list = []
                        for res_item in res:
                            res_item = ''.join(res_item)
                            result = res_item.split('\n')
                            result = [x.strip() for x in result if x.strip() != '']
                            teacher = result[1].split('[')[0]
                            address = result[2].split('[')[0]
                            weeks = re.findall(r'[(](.*?)[)]', result[2])[-1]
                            result[1] = weeks
                            result[2] = address
                            result.append(teacher)
                            new_course_list.append(result)
                        ex[k] = new_course_list
                    else:
                        res = v.split('\n')
                        new_course_list = []
                        course = res[0]
                        teacher = ''
                        for i in res[1:]:
                            address = ''
                            weeks = ''
                            if '-' in i and '(' in i:
                                address = i.split('(')[0]
                                weeks = re.findall(r'[(](.*?)[)]', i)[-1]
                            elif '[' in i and '-' not in i:
                                teacher = i.split('[')[0]
                            new_course = [course, weeks, address, teacher]
                            new_course_list.append(new_course)
                        ex[k] = new_course_list

            elif isinstance(v, str) and '\n' in v and ';' not in v and v.count('\n') < 3:
                res = v.split('\n')
                if '[' in res[1]:
                    teacher = res[1].split('[')[0]
                if '[' in res[2]:
                    address = res[2].split('[')[0]
                    weeks = res[2].split(']')[1]
                    weeks = re.findall(r'[(](.*?)[)]', weeks)[0]
                    res[1] = weeks
                    res[2] = address
                    res.append(teacher)
                if '[' not in res[2] and '(' in res[2]:
                    address = res[2].split('(')[0]
                    weeks = re.findall(r'[(](.*?)[)]', res[2])[0]
                    res[1] = weeks
                    res[2] = address
                    res.append(teacher)
                ex[k] = res

            elif isinstance(v, str) and v.count('\n') == 3:
                res = v.split(';')
                new_course_list = []
                for res_item in res:
                    result = res_item.split('\n')
                    result = [x.strip() for x in result if x.strip() != '']
                    teacher = result[1].split('[')[0]
                    address1 = result[2].split('[')[0]
                    weeks1 = re.findall(r'[(](.*?)[)]', result[2])[-1]
                    r1 = [result[0], weeks1, address1, teacher]
                    address2 = result[3].split('[')[0]
                    weeks2 = re.findall(r'[(](.*?)[)]', result[3])[-1]
                    r2 = [result[0], weeks2, address2, teacher]
                    new_course_list = [r1, r2]
                ex[k] = new_course_list
        for k, v in ex.items():
            if isinstance(v, list):
                for item in v:
                    if isinstance(item, list):
                        try:
                            week_str = item[1]
                            if '*' in item[0] and '**' not in item[0]:
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
                        except Exception as e:
                            pass

                    elif not isinstance(item, list) and not isinstance(v[-1], list):
                        if len(v) == 4:
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
                        else:
                            pass
        return ex

    def get_scdx_course_info(self, ex):
        jie1 = int(ex['class_sessions'])
        jie2 = jie1 + int(ex['continuing'])
        new_ex_list = []
        for jie in range(jie1, jie2):
            new_ex = {
                'jie': '',
            }

            weeks_dict = {
                1: 'Mon',
                2: 'Tues',
                3: 'Wed',
                4: 'Thur',
                5: 'Fri',
                6: 'Sat',
                7: 'Sun',
            }
            week_day = weeks_dict[ex['class_day']]
            course_name = ex['course_name']
            course_weeks = ex['course_weeks']
            course_address = ex['course_address']
            course_teacher = ex['course_teacher']
            course = [course_name, course_weeks, course_address, course_teacher]
            new_ex['jie'] = str(jie)
            new_ex[week_day] = course
            new_ex_list.append(new_ex)
        for ex in new_ex_list:
            for k, v in ex.items():
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
                    ex[k] = v
        return new_ex_list

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

    def scdx_schedule(self, uid, request_week):
        res_list = ScdxSchedule.query.filter_by(uid=uid).all()
        result = []
        current_week = get_current_week(SCDX_BEGIN_DATE, datetime.now().strftime('%Y-%m-%d'))
        for i in range(1, 14):
            data = {
                'jie': '',
                'Mon': '',
                'Tues': '',
                'Wed': '',
                'Thur': '',
                'Fri': '',
                'Sat': '',
                'Sun': ''
            }
            data['jie'] = str(i)
            result.append(data)
        for res in res_list:
            res_dict = res.to_dict()
            exce = ['id', 'uid', 'status']
            res_dict = black_list(res_dict, exce)
            res_dict_list = self.get_scdx_course_info(res_dict)
            for res_dict in res_dict_list:
                if request_week:
                    res_dict = self.get_request_schedule(res_dict, request_week)
                else:
                    res_dict = self.get_request_schedule(res_dict, current_week)
                for i in result:
                    if i['jie'] == res_dict['jie']:
                        i['current_week'] = current_week
                        i['total_weeks'] = SCDX_TOTAL_WEEKS
                        for k, v in res_dict.items():
                            if v:
                                i[k] = v
        return result

    def scdx_today_schedule(self, uid):
        res_list = ScdxSchedule.query.filter_by(uid=uid).all()
        result = []
        for i in range(1, 14):
            data = {
                'jie': '',
                'Mon': '',
                'Tues': '',
                'Wed': '',
                'Thur': '',
                'Fri': '',
                'Sat': '',
                'Sun': ''
            }
            data['jie'] = str(i)
            result.append(data)
        for res in res_list:
            res_dict = res.to_dict()
            exce = ['id', 'uid', 'status']
            res_dict = black_list(res_dict, exce)
            res_dict_list = self.get_scdx_course_info(res_dict)
            weekday = get_week_day(datetime.now())
            wonder = ['jie', weekday]
            for res_dict in res_dict_list:
                res_dict = white_list(res_dict, wonder)
                current_week = get_current_week(SCDX_BEGIN_DATE, datetime.now().strftime('%Y-%m-%d'))
                res_dict = self.get_request_schedule(res_dict, current_week)
                for i in result:
                    if i['jie'] == res_dict['jie']:
                        i.update(res_dict)
        return result

    def main(self, college, uid, request_week):
        if college == '西南交通大学':
            data = self.xnjd_schedule(uid, request_week)
            return data
        elif college == '四川师范大学':
            data = self.scsd_schedule(uid, request_week)
            return data
        elif college == '四川大学':
            data = self.scdx_schedule(uid, request_week)
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
        elif college == '四川大学':
            data = self.scdx_today_schedule(uid)
            return data
        else:
            info = {
                'status': 404,
                'msg': '需要参数college'
            }
            return info

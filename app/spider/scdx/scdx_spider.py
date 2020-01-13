import json
from pyquery import PyQuery as pq
from app.models.base import db
from app.models.scdx_next_term_schedule import ScdxNextTermSchedule
from app.models.scdx_schedule import ScdxSchedule
from app.models.user_score import UserScore
from app.models.user_total_score import UserTotalScore
from app.spider.spiderbase import SpiderBase
from utils import log


class ScdxSpider(SpiderBase):

    def __init__(self, session, xh):
        self.xh = xh  # 学号
        self.name = ''
        self.score = []
        self.schedule = []
        self.next_schedule = []
        self.college = '四川大学'
        self.session = session
        # self.score_url = 'http://zhjw.scu.edu.cn/student/integratedQuery/scoreQuery/allTermScores/index'
        self.schedule_url = "http://zhjw.scu.edu.cn/student/courseSelect/thisSemesterCurriculum/ajaxStudentSchedule/callback"
        self.next_schedule_url = "http://zhjw.scu.edu.cn/student/courseSelect/thisSemesterCurriculum/ajaxStudentSchedule/callback"
        self.score_data_url = "http://zhjw.scu.edu.cn/student/integratedQuery/scoreQuery/allTermScores/data"
        self.index = "http://zhjw.scu.edu.cn/"
        self.jidian_api = "http://zhjw.scu.edu.cn/main/academicInfo"
        self.total_jidian = ''

    def get_score(self):
        data = {
            'zxjxjhh': '',
            'kch': '',
            'kcm': '',
            'pageNum': 1,
            'pageSize': 200,

        }
        r = self.session.post(self.score_data_url, data)
        try:
            scores = json.loads(r.text)
            score_list = scores['list']['records']
            for i in score_list:
                xueqi = i[0]
                course = i[11]
                xuanxiu = i[15]
                score = i[8]
                xuefen = i[13]
                xishu = None
                jidian = None
                course_score = {
                    'xh': self.xh,
                    'name': self.name,
                    "course": course,
                    'xuanxiu': xuanxiu,
                    'score': score,
                    'jidian': jidian,
                    'xueqi': xueqi,
                    'xuefen': xuefen,
                    'xishu': xishu
                }
                self.score.append(course_score)
            return True
        except Exception as e:
            log(e, '*****未获取到考试成绩，可能本学期未进行过考试或未进行课程评价')
            return False

    # 本学期课表
    def get_schedule(self):
        r = self.session.get(self.index)
        page = pq(r.content)
        name = page('span.user-info')
        name = pq(name).text()
        self.name = name.split('，')[-1].replace(' ', '')
        res = self.session.get(self.schedule_url)
        try:
            schedule_infos = json.loads(res.text)['xkxx']
            for infos in schedule_infos:
                s = list(infos.values())
                for info in s:
                    schedule_infos = info['timeAndPlaceList']
                    course_teacher = info['attendClassTeacher']
                    for schedule_info in schedule_infos:
                        course_name = schedule_info['coureName']
                        class_day = schedule_info['classDay']
                        class_sessions = schedule_info['classSessions']
                        continuing = schedule_info['continuingSession']
                        course_weeks = schedule_info['weekDescription']
                        course_address = schedule_info['campusName'] + \
                                         schedule_info['teachingBuildingName'] + \
                                         schedule_info['classroomName']
                        schedules = {
                            'xh': self.xh,
                            'name': self.name,
                            'course_teacher': course_teacher,
                            'course_name': course_name,
                            'class_day': class_day,
                            'class_sessions': class_sessions,
                            'continuing': continuing,
                            'course_weeks': course_weeks,
                            'course_address': course_address
                        }
                        self.schedule.append(schedules)
        except Exception as e:
            log(e, "*****获取课表信息失败")

    def save_score(self, uid):
        status = self.get_score()
        with db.auto_commit():
            db.session.query(UserScore).filter(UserScore.uid == uid).delete()
        if status:
            for i in self.score:
                user_score = UserScore()
                score_dict = i
                score_dict['uid'] = uid
                user_score.setattr(score_dict)
                with db.auto_commit():
                    db.session.add(user_score)
            return True
        else:
            return False

    def save_schedule(self, uid):
        self.get_schedule()
        with db.auto_commit():
            db.session.query(ScdxSchedule).filter(ScdxSchedule.uid == uid).delete()
        for i in self.schedule:
            user_schedule = ScdxSchedule()
            schedule_dict = i
            schedule_dict['uid'] = uid
            user_schedule.setattr(schedule_dict)
            with db.auto_commit():
                db.session.add(user_schedule)

    def save_total_score(self, uid):
        data1 = {
            'falg': ''
        }
        r = self.session.post(self.jidian_api, data1)
        info = json.loads(r.text)
        for i in info:
            self.total_jidian = i['gpa'] if isinstance(i, dict) else None
        data = {
            'xh': self.xh,
            'name': self.name,
            'average_score': None,
            'average_jidian': float(self.total_jidian),
            'total_xuefen': None
        }
        data['uid'] = uid
        with db.auto_commit():
            db.session.query(UserTotalScore).filter(UserTotalScore.uid == uid).delete()
        total_score = UserTotalScore()
        with db.auto_commit():
            total_score.setattr(data)
            db.session.add(total_score)

    # 下学期课表
    def get_next_term_schedule(self):
        r = self.session.get(self.index)
        page = pq(r.content)
        name = page('span.user-info')
        name = pq(name).text()
        self.name = name.split('，')[-1].replace(' ', '')

        data = {
            "planCode": "2019-2020-2-1"
        }
        res = self.session.post(self.next_schedule_url, data)
        try:
            schedule_infos = json.loads(res.text)['xkxx']
            for infos in schedule_infos:
                s = list(infos.values())
                for info in s:
                    schedule_infos = info['timeAndPlaceList']
                    course_teacher = info['attendClassTeacher']
                    for schedule_info in schedule_infos:
                        course_name = schedule_info['coureName']
                        class_day = schedule_info['classDay']
                        class_sessions = schedule_info['classSessions']
                        continuing = schedule_info['continuingSession']
                        course_weeks = schedule_info['weekDescription']
                        course_address = schedule_info['campusName'] + \
                                         schedule_info['teachingBuildingName'] + \
                                         schedule_info['classroomName']
                        schedules = {
                            'xh': self.xh,
                            'name': self.name,
                            'course_teacher': course_teacher,
                            'course_name': course_name,
                            'class_day': class_day,
                            'class_sessions': class_sessions,
                            'continuing': continuing,
                            'course_weeks': course_weeks,
                            'course_address': course_address
                        }
                        self.next_schedule.append(schedules)
        except Exception as e:
            log(e, "*****获取课表信息失败")

    def save_next_term_schedule(self, uid):
        self.get_next_term_schedule()
        with db.auto_commit():
            db.session.query(ScdxNextTermSchedule).filter(ScdxNextTermSchedule.uid == uid).delete()
        for i in self.next_schedule:
            user_schedule = ScdxNextTermSchedule()
            schedule_dict = i
            schedule_dict['uid'] = uid
            user_schedule.setattr(schedule_dict)
            with db.auto_commit():
                db.session.add(user_schedule)

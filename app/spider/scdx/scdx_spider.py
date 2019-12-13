import json

from pyquery import PyQuery as pq
from app.models.base import db
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
        self.college = '四川大学'
        self.session = session
        # self.score_url = 'http://zhjw.scu.edu.cn/student/integratedQuery/scoreQuery/allTermScores/index'
        self.schedule_url = "http://zhjw.scu.edu.cn/student/courseSelect/thisSemesterCurriculum/ajaxStudentSchedule/callback"
        self.score_data_url = "http://202.115.47.141/student/integratedQuery/scoreQuery/allTermScores/data"
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
        scores = json.loads(r.text)
        try:
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
        if status:
            for i in self.score:
                user_score = UserScore()
                score_dict = i
                score_dict['uid'] = uid
                user_score.setattr(score_dict)
                find_user = UserScore.query.filter_by(
                    course=score_dict['course'], uid=uid, xueqi=score_dict['xueqi']
                ).first()
                if find_user:
                    with db.auto_commit():
                        find_user.setattr(score_dict)
                else:
                    with db.auto_commit():
                        db.session.add(user_score)
            return True
        else:
            return False

    def save_schedule(self, uid):
        self.get_schedule()
        for i in self.schedule:
            user_schedule = ScdxSchedule()
            schedule_dict = i
            schedule_dict['uid'] = uid
            user_schedule.setattr(schedule_dict)
            update_schedule = ScdxSchedule.query.filter_by(class_day=schedule_dict['class_day'],
                                                           course_name=schedule_dict['course_name'],
                                                           class_sessions=schedule_dict['class_sessions'],
                                                           uid=uid).first()
            if update_schedule:
                with db.auto_commit():
                    update_schedule.setattr(schedule_dict)
            else:
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
        total_score = UserTotalScore()
        user_info = UserTotalScore.query.filter_by(uid=uid).first()
        if user_info:
            with db.auto_commit():
                user_info.setattr(data)
        else:
            with db.auto_commit():
                total_score.setattr(data)
                db.session.add(total_score)

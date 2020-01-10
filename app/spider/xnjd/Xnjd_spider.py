from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
from app.models.base import db
from app.models.user_schedule import UserSchedule
from app.models.user_score import UserScore
from app.models.xnjd_next_term_schedule import XnjdNextTermSchedule
from app.spider.spiderbase import SpiderBase
from utils import log


class XnjdSpider(SpiderBase):

    def __init__(self, session):
        self.xh = ''  # 学号
        self.name = ''
        self.score = []
        self.schedule = []
        self.next_schedule = []
        self.college = '西南交通大学'
        self.session = session
        self.score_url = 'http://jwc.swjtu.edu.cn/vatuu/StudentScoreInfoAction?setAction=studentMarkFromTerm'
        self.schedule_url = "http://jwc.swjtu.edu.cn/vatuu/CourseAction?setAction=userCourseScheduleTable&viewType=studentQueryCourseList&selectTableType=ThisTerm&queryType=student"
        self.next_schedule_url = "http://jwc.swjtu.edu.cn/vatuu/CourseAction?setAction=userCourseSchedule&selectTableType=NextTerm"

    def get_score(self):
        score_html = self.session.get(self.score_url)
        soup = BeautifulSoup(score_html.content, 'lxml')
        try:
            tr = soup.find('table', class_='table_border').find_all('tr')
            for j in tr[1:]:
                td = j.find_all('td')
                course = td[4].get_text().strip()
                xuanxiu = td[6].get_text().strip()
                xueqi = td[1].get_text().strip()
                xuefen = td[7].find(attrs={'value': True}).get('value')
                score = td[9].find(attrs={'value': True}).get('value')
                jidian = td[12].find(attrs={'value': True}).get('value')
                xishu = td[13].find(attrs={'value': True}).get('value')
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
        schedule_html = self.session.get(self.schedule_url)
        page = pq(schedule_html.content)
        info = page('.form-span strong span').text()
        # res = info.split(' ')[0]
        res = info[:14]
        self.xh = res[:10]
        self.name = res[10:]
        if '\xa0' in self.name:
            self.name = self.name.replace(u'\xa0', '')
        soup = BeautifulSoup(schedule_html.content, 'lxml')
        try:
            tr = soup.find('table', class_='table_border').find_all('tr')
            for j in tr[1:]:
                td = j.find_all('td')
                jie = td[0].get_text().strip()
                mon = td[2].get_text().strip()
                tues = td[3].get_text().strip()
                wed = td[4].get_text().strip()
                thur = td[5].get_text().strip()
                fri = td[6].get_text().strip()
                sat = td[7].get_text().strip()
                sun = td[8].get_text().strip()
                schedule = {
                    'xh': self.xh,
                    'name': self.name,
                    'jie': jie,
                    'Mon': mon,
                    'Tues': tues,
                    'Wed': wed,
                    'Thur': thur,
                    'Fri': fri,
                    'Sat': sat,
                    'Sun': sun
                }
                self.schedule.append(schedule)
        except Exception as e:
            log(e, "*****获取课表信息失败")

    def get_next_term_schedule(self):
        schedule_html = self.session.get(self.next_schedule_url)
        soup = BeautifulSoup(schedule_html.content, 'lxml')
        try:
            tr = soup.find('table', class_='table_border').find_all('tr')
            for j in tr[1:]:
                td = j.find_all('td')
                course_name = td[4].get_text().strip()
                course_teacher = td[7].get_text().strip()
                course_infos = td[10].get_text().strip()
                weeks_dict = {
                    "星期一": 'Mon',
                    "星期二": 'Tues',
                    "星期三": 'Wed',
                    "星期四": 'Thur',
                    "星期五": 'Fri',
                    "星期六": 'Sat',
                    "星期日": 'Sun',
                }
                if course_infos.count('节') == 1:
                    course_info = course_infos.split('节')[0]
                    course_address = course_infos.split('节')[-1].strip()
                    # if " " in course_info:
                    course_weeks = course_info.split(' ')[0]
                    class_day = course_info.split(' ')[1]
                    course_continue = course_info.split(' ')[-1]
                    class_day = weeks_dict[class_day]
                    schedules = {
                        'xh': self.xh,
                        'name': self.name,
                        'course_teacher': course_teacher,
                        'course_name': course_name,
                        'class_day': class_day,
                        'course_continue': course_continue,
                        'course_weeks': course_weeks,
                        'course_address': course_address
                    }
                    self.next_schedule.append(schedules)
                elif "节" in course_infos:
                    course_info = course_infos.replace('\t', '')
                    course_info_list = course_info.split('\r\n')
                    course_info_list = [x for x in course_info_list if x != '']
                    index = [0, 2, 4, 6]
                    for i in index:
                        if i < len(course_info_list):
                            course_info = course_info_list[i]
                            course_address = course_info_list[i+1]
                            course_weeks = course_info.split(' ')[0]
                            class_day = course_info.split(' ')[1]
                            course_continue = course_info.split(' ')[-1].replace('节', '')
                            class_day = weeks_dict[class_day]
                            schedules = {
                                'xh': self.xh,
                                'name': self.name,
                                'course_teacher': course_teacher,
                                'course_name': course_name,
                                'class_day': class_day,
                                'course_continue': course_continue,
                                'course_weeks': course_weeks,
                                'course_address': course_address
                            }
                            self.next_schedule.append(schedules)
                        else:
                            break
        except Exception as e:
            log(e, "*****获取下学期课表信息失败")

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
        schedule = UserSchedule.query.filter_by(uid=uid).all()
        for i in schedule:
            with db.auto_commit():
                db.session.delete(i)
        for i in self.schedule:
            user_schedule = UserSchedule()
            schedule_dict = i
            schedule_dict['uid'] = uid
            user_schedule.setattr(schedule_dict)
            update_schedule = UserSchedule.query.filter_by(jie=schedule_dict['jie'], uid=uid).first()
            if update_schedule:
                with db.auto_commit():
                    update_schedule.setattr(schedule_dict)
            else:
                with db.auto_commit():
                    db.session.add(user_schedule)

    def save_next_term_schedule(self, uid):
        self.get_next_term_schedule()
        schedule = XnjdNextTermSchedule.query.filter_by(uid=uid).all()
        for i in schedule:
            with db.auto_commit():
                db.session.delete(i)
        for i in self.next_schedule:
            user_schedule = XnjdNextTermSchedule()
            schedule_dict = i
            schedule_dict['uid'] = uid
            user_schedule.setattr(schedule_dict)
            update_schedule = XnjdNextTermSchedule.query.filter_by(class_day=schedule_dict['class_day'],
                                                                   course_name=schedule_dict['course_name'],
                                                                   course_continue=schedule_dict['course_continue'],
                                                                   uid=uid).first()
            if update_schedule:
                with db.auto_commit():
                    update_schedule.setattr(schedule_dict)
            else:
                with db.auto_commit():
                    db.session.add(user_schedule)

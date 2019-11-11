from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
from app.models.base import db
from app.models.user_schedule import UserSchedule
from app.models.user_score import UserScore
from utils import log


class XnjdSpider:

    def __init__(self, session):
        self.xh = ''  # 学号
        self.name = ''
        self.score = []
        self.schedule = []
        self.college = '西南交通大学'
        self.session = session

    def get_score(self):
        score_url = 'http://jwc.swjtu.edu.cn/vatuu/StudentScoreInfoAction?setAction=studentMarkFromTerm'
        score_html = self.session.get(score_url)

        page = pq(score_html.content)
        info = page('.instruction-div.clearfix div strong').text()
        res = info.split(' ')[0]
        self.xh = res[:9]
        self.name = res[10:]
        if '\xa0' in self.name:
            self.name = self.name.replace(u'\xa0', '')

        soup = BeautifulSoup(score_html.content, 'lxml')
        tr = soup.find('table', class_='table_border').find_all('tr')
        try:
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

        except Exception as e:
            log(e, '*****未获取到考试成绩，可能本学期未进行过考试')
        # print(self.score)

    def get_schedule(self):
        schedule_url = "http://jwc.swjtu.edu.cn/vatuu/CourseAction?setAction=userCourseScheduleTable&viewType=studentQueryCourseList&selectTableType=ThisTerm&queryType=student"
        schedule_html = self.session.get(schedule_url)

        soup = BeautifulSoup(schedule_html.content, 'lxml')
        tr = soup.find('table', class_='table_border').find_all('tr')
        try:
            for j in tr[1:]:
                td = j.find_all('td')
                jie = td[0].get_text().strip()
                mon = td[1].get_text().strip()
                tues = td[2].get_text().strip()
                wed = td[3].get_text().strip()
                thur = td[4].get_text().strip()
                fri = td[5].get_text().strip()
                sat = td[6].get_text().strip()
                sun = td[7].get_text().strip()
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

    def save_score(self, uid):
        self.get_score()
        for i in self.score:
            user_score = UserScore()
            score_dict = i
            score_dict['uid'] = uid
            user_score.setattr(score_dict)
            # 判断是否有挂科成绩，如果有，进行更新。
            find_user = UserScore.query.filter_by(course=score_dict['course'], uid=uid, xueqi=score_dict['xueqi']).first()
            if find_user:
                with db.auto_commit():
                    find_user.setattr(score_dict)
            else:
                with db.auto_commit():
                    db.session.add(user_score)

    def save_schedule(self, uid):
        self.get_schedule()
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

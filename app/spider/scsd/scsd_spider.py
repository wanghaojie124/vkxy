import copy

from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
from app.models.base import db
from app.models.user_schedule import UserSchedule
from app.models.user_score import UserScore
from app.models.user_total_score import UserTotalScore
from app.spider.spiderbase import SpiderBase
from utils import log


class ScsdSpider(SpiderBase):

    def __init__(self, session, domain, username):
        self.xh = ''  # 学号
        self.name = ''
        self.score = []
        self.schedule = []
        self.college = '四川师范大学'
        self.session = session
        self.score_url = domain + '/ScoreQuery/wp_StudentElectCourseScore_All_Print.aspx?Id={}'.format(username)
        self.schedule_url = domain + '/ScheduleManage/wp_Schedule_ForSelfStudent.aspx'
        self.total_score_url = domain + '/Index/wp_StudentIndex.aspx'

    def get_score(self):
        score_html = self.session.get(self.score_url)
        soup = BeautifulSoup(score_html.content, 'lxml')
        infos = soup.find('span', id='ctl00_ctl00_body_body_lblSubTitle').find_all('strong')
        self.xh = infos[0].text
        self.name = infos[1].text
        try:
            tr = soup.find('tbody').find_all('tr')
            for j in tr:
                td = j.find_all('td')
                xueqi = td[1].get_text().strip()
                course = td[3].get_text().strip()
                xuefen = td[5].get_text().strip()
                score = td[6].get_text().strip()
                jidian = td[-1].get_text().strip()
                kind = td[4].get_text().strip()
                if '必' in kind:
                    xuanxiu = '必'
                elif '选' in kind:
                    xuanxiu = '选'
                else:
                    xuanxiu = kind
                course_score = {
                    'xh': self.xh,
                    'name': self.name,
                    "course": course,
                    'xuanxiu': xuanxiu,
                    'score': score,
                    'jidian': jidian,
                    'xueqi': xueqi,
                    'xuefen': xuefen,
                }
                self.score.append(course_score)
            return True
        except Exception as e:
            log(e, '*****未获取到考试成绩，可能本学期未进行过考试或未进行课程评价')
            return False

    def get_total_score(self, uid):
        try:
            score_html = self.session.get(self.score_url)
            soup = BeautifulSoup(score_html.content, 'lxml')
            infos = soup.find('span', id='ctl00_ctl00_body_body_lblSubTitle').find_all('strong')
            self.xh = infos[0].text
            self.name = infos[1].text
            info_html = self.session.get(self.total_score_url)
            page = pq(info_html.content)
            table = page('table.table4')
            average_score = pq(table)('tr')[1][1]
            average_score = pq(average_score).text()
            average_jidian = pq(table)('tr')[1][2]
            average_jidian = pq(average_jidian).text()
            total_xuefen = pq(table)('tr')[6][1]
            total_xuefen = pq(total_xuefen).text()
            data = {
                'xh': self.xh,
                'name': self.name,
                'average_score': average_score,
                'average_jidian': average_jidian,
                'total_xuefen': total_xuefen,
            }
            return data
        except IndexError as e:
            log('***', '师大' + uid, '获取total_score错误', e)

    def get_schedule(self):
        schedule_html = self.session.get(self.schedule_url)
        page = pq(schedule_html.content)
        trs = page('#divScheduleTable table tbody tr')
        tr_len = 0
        try:
            for tr in trs:
                if tr_len == 0:
                    tr_len = len(tr)
                if tr_len == len(tr):
                    jie = tr[1].text.split('节')[0]
                    mon = pq(tr[2]).text()
                    tues = pq(tr[3]).text()
                    wed = pq(tr[4]).text()
                    thur = pq(tr[5]).text()
                    fri = pq(tr[6]).text()
                    sat = pq(tr[7]).text()
                    sun = pq(tr[8]).text()
                    schedule = {
                        'name': self.name,
                        'xh': self.xh,
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
                elif len(tr) == tr_len - 1:
                    jie = tr[0].text.split('节')[0]
                    mon = pq(tr[1]).text()
                    tues = pq(tr[2]).text()
                    wed = pq(tr[3]).text()
                    thur = pq(tr[4]).text()
                    fri = pq(tr[5]).text()
                    sat = pq(tr[6]).text()
                    sun = pq(tr[7]).text()
                    schedule = {
                        'name': self.name,
                        'xh': self.xh,
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
                elif len(tr) != tr_len and len(tr) != 1:
                    jie = tr[0].text.split('节')[0]
                    schedule = copy.deepcopy(self.schedule[-1])
                    schedule['jie'] = jie
                    self.schedule.append(schedule)
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
        if not self.xh:
            self.get_score()
        schedule = UserSchedule.query.filter_by(uid=uid).all()
        for i in schedule:
            with db.auto_commit():
                db.session.delete(i)
        for i in self.schedule:
            user_schedule = UserSchedule()
            schedule_dict = i
            schedule_dict['uid'] = uid
            schedule_dict['xh'] = self.xh
            schedule_dict['name'] = self.name
            user_schedule.setattr(schedule_dict)
            update_schedule = UserSchedule.query.filter_by(jie=schedule_dict['jie'], uid=uid).first()
            if update_schedule:
                with db.auto_commit():
                    update_schedule.setattr(schedule_dict)
            else:
                with db.auto_commit():
                    db.session.add(user_schedule)

    def save_total_score(self, uid):
        data = self.get_total_score(uid)
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
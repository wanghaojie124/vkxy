import copy
import re

from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
from app.models.base import db
from app.models.user_next_term_schedule import UserNextTermSchedule
from app.models.user_schedule import UserSchedule
from app.models.user_score import UserScore
from app.models.user_total_score import UserTotalScore
from app.spider.spiderbase import SpiderBase
from app.spider.zjcm.zjcm_calendar import ZJCM_BEGIN_DATE
from utils import log, getuser_agent


class ZjcmSpider(SpiderBase):

    def __init__(self, session, username):
        self.xh = username  # 学号
        self.name = ''
        self.score = []
        self.schedule = []
        self.next_term_schedule = []
        self.college = '浙江传媒学院'
        self.session = session
        self.index_url = "http://xuanke.cuz.edu.cn/xs_main.aspx?xh={}".format(username)
        self.score_url = "http://xuanke.cuz.edu.cn/xscjcx.aspx?"
        self.schedule_url = "http://xuanke.cuz.edu.cn/xskbcx.aspx?"

    def get_score(self):
        index_html = self.session.get(self.index_url)
        soup = BeautifulSoup(index_html.content, 'html.parser')
        name = soup.find('span', id='xhxm').get_text()
        self.name = name.split('同学')[0]

        score_url = self.score_url + "xh={}&xm={}&gnmkdm={}".format(self.xh, self.name, 'N121605')
        headers = {
            "User-Agent": getuser_agent(),
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "http://xuanke.cuz.edu.cn/xs_main.aspx?xh={}".format(self.xh)
        }
        self.session.headers.update(headers)
        data = {
            "ddlXN": "",
            "ddlXQ": "",
            "__VIEWSTATE": "",
            "__VIEWSTATEGENERATOR": "",
            "__EVENTTARGET": "",
            "__EVENTARGUMENT": "",
            "ddl_kcxz": '',
            "btn_zcj": "历年成绩",
            "hidLanguage": ""
        }
        resp = self.session.get(score_url)
        soup = BeautifulSoup(resp.text, "lxml")
        data["__VIEWSTATEGENERATOR"] = soup.find('input', id='__VIEWSTATEGENERATOR', attrs={'value': True}).get('value', '')
        data["__VIEWSTATE"] = soup.find('input', id='__VIEWSTATE', attrs={'value': True}).get('value', '')
        data["__EVENTTARGET"] = soup.find('input', id='__EVENTTARGET', attrs={'value': True}).get('value', '')
        data["__EVENTARGUMENT"] = soup.find('input', id='__EVENTARGUMENT', attrs={'value': True}).get('value', '')

        score_html = self.session.post(score_url, data)
        soup = BeautifulSoup(score_html.content, 'html.parser')
        try:
            tr = soup.find('table').find_all('tr')
            for j in tr[1:]:
                td = j.find_all('td')
                xueqi = td[0].get_text().strip() + "-" + td[1].get_text().strip()
                course = td[3].get_text().strip()
                xuefen = td[6].get_text().strip()
                score = td[12].get_text().strip()
                jidian = td[7].get_text().strip()
                kind = td[4].get_text().strip()
                make_up = td[-5].get_text().strip()
                rebuild = td[-4].get_text().strip()
                if make_up or rebuild:
                    score = make_up
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

    def get_schedule(self):
        index_html = self.session.get(self.index_url)
        soup = BeautifulSoup(index_html.content, 'html.parser')
        name = soup.find('span', id='xhxm').get_text()
        self.name = name.split('同学')[0]

        schedule_url = self.schedule_url + "xh={}&xm={}&gnmkdm={}".format(self.xh, self.name, 'N121603')
        headers = {
            "User-Agent": getuser_agent(),
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "http://xuanke.cuz.edu.cn/xs_main.aspx?xh={}".format(self.xh)
        }
        self.session.headers.update(headers)
        schedule_html = self.session.get(schedule_url)
        page = pq(schedule_html.text)
        trs = page('tr')
        tr_len = 0
        try:
            for tr in trs[2:14]:
                if tr_len == 0:
                    tr_len = len(tr)
                if tr_len == len(tr):
                    jie = tr[1].text
                    jie = re.findall(r'\d+', jie)
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
                    jie = tr[0].text
                    jie = re.findall(r'\d+', jie)
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
                    jie = tr[0].text
                    jie = re.findall(r'\d+', jie)
                    schedule = copy.deepcopy(self.schedule[-1])
                    schedule['jie'] = jie
                    self.schedule.append(schedule)
        except Exception as e:
            log(e, "*****获取课表信息失败")

    def get_next_schedule(self):
        index_html = self.session.get(self.index_url)
        soup = BeautifulSoup(index_html.content, 'html.parser')
        name = soup.find('span', id='xhxm').get_text()
        self.name = name.split('同学')[0]

        schedule_url = self.schedule_url + "xh={}&xm={}&gnmkdm={}".format(self.xh, self.name.encode('utf-8'), 'N121603')
        headers = {
            "User-Agent": getuser_agent(),
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "http://xuanke.cuz.edu.cn/xs_main.aspx?xh={}".format(self.xh)
        }
        self.session.headers.update(headers)
        data = {
            "__EVENTTARGET": "xqd",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": "",
            "__VIEWSTATEGENERATOR": '',
            "xnd": "2019-2020",
            "xqd": "2"
        }
        info_html = self.session.get(schedule_url)
        soup = BeautifulSoup(info_html.text, 'html.parser')
        data["__VIEWSTATEGENERATOR"] = soup.find('input', id='__VIEWSTATEGENERATOR', attrs={'value': True}).get('value', '')
        data["__VIEWSTATE"] = soup.find('input', id='__VIEWSTATE', attrs={'value': True}).get('value', '')
        data["__LASTFOCUS"] = soup.find('input', id='__EVENTTARGET', attrs={'value': True}).get('value', '')
        data["__EVENTARGUMENT"] = soup.find('input', id='__EVENTARGUMENT', attrs={'value': True}).get('value', '')
        headers = {
            "User-Agent": getuser_agent(),
            "X-Requested-With": "XMLHttpRequest",
            "Referer": schedule_url
        }
        self.session.headers.update(headers)
        schedule_html = self.session.post(schedule_url, data)
        page = pq(schedule_html.text)
        print(page)
        trs = page('tr')
        tr_len = 0
        try:
            for tr in trs[2:13]:
                if tr_len == 0:
                    tr_len = len(tr)
                if tr_len == len(tr):
                    jie = tr[1].text()
                    jie = re.findall(r'\d+', jie)
                    mon = pq(tr[2]).text()
                    tues = pq(tr[3]).text()
                    wed = pq(tr[4]).text()
                    thur = pq(tr[5]).text()
                    fri = pq(tr[6]).text()
                    sat = pq(tr[7]).text()
                    sun = pq(tr[-1]).text()
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
                    self.next_term_schedule.append(schedule)
                elif len(tr) == tr_len - 1:
                    jie = tr[0].text
                    jie = re.findall(r'\d+', jie)
                    print(jie)
                    mon = pq(tr[1]).text()
                    tues = pq(tr[2]).text()
                    wed = pq(tr[3]).text()
                    thur = pq(tr[4]).text()
                    fri = pq(tr[5]).text()
                    sat = pq(tr[6]).text()
                    sun = pq(tr[-1]).text()
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
                    self.next_term_schedule.append(schedule)
                elif len(tr) != tr_len and len(tr) != 1:
                    jie = tr[0].text
                    jie = re.findall(r'\d+', jie)
                    schedule = copy.deepcopy(self.schedule[-1])
                    schedule['jie'] = jie
                    self.next_term_schedule.append(schedule)
        except Exception as e:
            log(e, "*****获取下学期课表信息失败")

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
            db.session.query(UserSchedule).filter(UserSchedule.uid == uid).delete()
        for i in self.schedule:
            user_schedule = UserSchedule()
            schedule_dict = i
            schedule_dict['uid'] = uid
            schedule_dict['xh'] = self.xh
            schedule_dict['name'] = self.name
            user_schedule.setattr(schedule_dict)
            with db.auto_commit():
                db.session.add(user_schedule)

    def save_next_term_schedule(self, uid):
        self.get_next_schedule()
        with db.auto_commit():
            db.session.query(UserNextTermSchedule).filter(UserNextTermSchedule.uid == uid).delete()
        for i in self.next_term_schedule:
            user_schedule = UserNextTermSchedule()
            schedule_dict = i
            schedule_dict['uid'] = uid
            schedule_dict['xh'] = self.xh
            schedule_dict['name'] = self.name
            user_schedule.setattr(schedule_dict)
            with db.auto_commit():
                db.session.add(user_schedule)

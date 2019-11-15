import time
from threading import Thread
from bs4 import BeautifulSoup
from flask import current_app
from utils import log


class Assess:
    # 评课url
    assess_list_url = 'http://jwc.swjtu.edu.cn/vatuu/AssessAction?setAction=list'
    # 提交url
    post_url = 'http://jwc.swjtu.edu.cn/vatuu/AssessAction'
    # 完成查看成绩url GET方法
    finish_url = 'http://jwc.swjtu.edu.cn/vatuu/StudentScoreInfoAction?setAction=studentScoreQuery&viewType=studentScore&orderType=submitDate&orderValue=desc'
    assess_list = []
    domain = "http://jwc.swjtu.edu.cn"
    assess_list = []

    def get_data(self, url, session):
        data = {
            'answer': '',
            'scores': '_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0_5.0__',
            'percents': '_10.0_10.0_10.0_10.0_10.0_10.0_10.0_10.0_10.0_10.0_0.0_0.0_0.0_0.0_0.0_0.0_0.0_0.0',
            'assess_id': '',
            'templateFlag': 0,
            't': 0.923362231864278,
            'keyword': 'null',
            # id为问题id
            'id': '',
            'logId': '',
            'setAction': '',
            'teacherId': ''
        }
        r = session.get(url=url)
        soup = BeautifulSoup(r.content, 'lxml')
        form = soup.find('form', id='answerForm')
        assess_id = form.find('input', attrs={'value': True}).get('value')
        data['assess_id'] = assess_id

        info = soup.find('form').find_next('form').find_all('input')
        values = {}
        for i in info:
            value = i.get('value')
            key = i.get('name')
            values[key] = value
        for k, v in values.items():
            if v:
                data[k] = v

        questions = ""
        percents = ""
        question_divs = form.find_all('div', class_='post-problem questionDiv')
        for div in question_divs:
            question = div.find('input', attrs={'value': True}).get('value')
            perc = div.find('input', attrs={'value': True}).get('perc')
            questions = questions + "_" + question
            percents = percents + "_" + perc

        answers = ""
        scores = ""
        answer_divs = form.find_all('div', class_='answerDiv questionDiv')
        for div in answer_divs:
            answer = div.find('input', attrs={'value': True}).get('value')
            score = div.find('input', attrs={'value': True}).get('score')
            answers = answers + "_" + answer
            scores = scores + "_" + score

        scores = scores + "__"
        answers = answers + "_无_无"
        data['answer'] = answers
        data['scores'] = scores
        data['percents'] = percents
        data['id'] = questions

        return data

    def get_assess_list(self, session):
        r = session.get(url=self.assess_list_url)
        with open('test.html', 'wb') as f:
            f.write(r.content)

        soup = BeautifulSoup(r.content, 'lxml')
        tr = soup.find('table', id='table3').find_all('tr')
        for j in tr[1:]:
            td = j.find_all('td')
            link = td[-1].find('a')
            if link:
                link = link.get('href')
                link = self.domain + link[2:]
                self.assess_list.append(link)

    def post_assess(self, session, data):
        r = session.post(self.post_url, data)
        log(r.content.decode())

    def assess_async(self, app, uid, session):
        with app.app_context():
            try:
                for url in self.assess_list:
                    data = self.get_data(url, session)
                    time.sleep(61)
                    self.post_assess(session, data)
                session.get(self.finish_url)
            except Exception as e:
                log(uid, '*****异步评课', e)

    # 异步存储数据入口函数
    def assess(self, uid, session):
        app = current_app._get_current_object()
        thr = Thread(target=self.assess_async, args=[app, uid, session])
        thr.start()
        log(uid, "开启新线程评课")

    def main(self, uid, session):
        self.get_assess_list(session)
        self.assess(uid, session)


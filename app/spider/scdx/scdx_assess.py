import json
import time
from threading import Thread
from bs4 import BeautifulSoup
from flask import current_app

from app.spider.scdx.scdx_spider import ScdxSpider
from app.spider.spiderbase import SpiderBase
from utils import log


class ScdxAssess(SpiderBase):
    # 获取待评价课程
    assess_page = "http://202.115.47.141/student/teachingEvaluation/teachingEvaluation/evaluationPage"
    # 获取打分data
    get_assess_list_url = "http://202.115.47.141/student/teachingEvaluation/teachingEvaluation/search"
    # 提交打分rul
    assess_url = "http://202.115.47.141/student/teachingEvaluation/teachingEvaluation/evaluation"
    assess_list = []
    course = []

    def get_data(self, data, session):
        r = session.post(self.assess_page, data)
        soup = BeautifulSoup(r.content, 'lxml')
        try:
            token_value = soup.find('input', id='tokenValue').get('value')
            assess_data = {
                'tokenValue': token_value,
                'questionnaireCode': data['questionnaireCode'],
                'evaluationContentNumber': data['evaluationContentNumber'],
                'evaluatedPeopleNumber': data['evaluatedPeopleNumber'],
                'count': '0',
                'zgpj': '暂无建议'
            }
            answer_id = soup.find_all('input', class_='ace')
            answer_id_list = []
            for i in answer_id:
                answer_id = i.get('name')
                answer_id_list.append(answer_id)
            answer_id_list = set(answer_id_list)
            for i in answer_id_list:
                assess_data[i] = '10_1'
            return assess_data
        except Exception as e:
            log(e)

    def get_course_list(self, session):
        r = session.get(url=self.get_assess_list_url)
        infos = json.loads(r.text)['data']
        for i in infos:
            if i['isEvaluated'] == '否':
                self.course.append(i['evaluationContent'])

    def get_assess_list(self, session):
        r = session.get(url=self.get_assess_list_url)
        infos = json.loads(r.text)['data']
        for i in infos:
            if i['isEvaluated'] == '否':
                data = {
                    'evaluatedPeople': '',
                    'evaluatedPeopleNumber': '',
                    'questionnaireCode': '',
                    'questionnaireName': '',
                    'evaluationContentNumber': '',
                    'evaluationContentContent': '',
                }
                data['evaluatedPeople'] = i['evaluatedPeople']
                data['evaluatedPeopleNumber'] = i['id']['evaluatedPeople']
                data['questionnaireCode'] = i['id']['questionnaireCoding']
                data['questionnaireName'] = i['questionnaire']['questionnaireName']
                data['evaluationContentNumber'] = i['id']['evaluationContentNumber']
                self.assess_list.append(data)

    def post_assess(self, session, data, uid):
        # TODO 如果启动代理ip，时效3分钟，需要此处更换代理
        r = session.post(self.assess_url, data)
        log(uid, '*****提交了数据', r.status_code)

    def assess_async(self, app, uid, session, xh):
        with app.app_context():
            if len(self.assess_list) == 0:
                self.get_assess_list(session)
            else:
                pass
            total = len(self.assess_list)
            i = 0
            while len(self.assess_list) > 0:
                for data in self.assess_list:
                    assess_data = self.get_data(data, session)
                    time.sleep(11)
                    try:
                        self.post_assess(session, assess_data, uid)
                        i += 1
                        self.assess_list.remove(data)
                        log('******已进行', i, '总共', total, '剩余', len(self.assess_list))
                    except Exception as e:
                        log(uid, '*****异步评课', e, '准备进行下次评课*****')
            scdx = ScdxSpider(session, xh)
            scdx.save_score(uid)
            scdx.save_next_term_schedule(uid)

    # 异步存储数据入口函数
    def assess(self, uid, session, xh):
        app = current_app._get_current_object()
        thr = Thread(target=self.assess_async, args=[app, uid, session, xh])
        thr.start()
        log(uid, "开启新线程评课")

    def main(self, uid, session, xh):
        self.assess(uid, session, xh)
        self.get_course_list(session)

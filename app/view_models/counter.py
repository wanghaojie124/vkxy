from app.models.user_score import UserScore
from utils import log


class Counter:
    # 川大分数转为绩点计算方法
    def scdx_score_to_jidian(self, score):
        if score >= 95:
            grade_point = 4
        elif score >= 90:
            grade_point = 3.8
            per_score = (4-3.8)/(95-90)
            grade_point += (score-90)*per_score
            grade_point = float('%.2f' % grade_point)
        elif score >= 85:
            grade_point = 3.6
            per_score = (3.8 - 3.6) / (90 - 85)
            grade_point += (score - 85) * per_score
            grade_point = float('%.2f' % grade_point)
        elif score >= 80:
            grade_point = 3.2
            per_score = (3.6 - 3.2) / (85 - 80)
            grade_point += (score - 80) * per_score
            grade_point = float('%.2f' % grade_point)
        elif score >= 75:
            grade_point = 2.7
            per_score = (3.2 - 2.7) / (80 - 75)
            grade_point += (score - 75) * per_score
            grade_point = float('%.2f' % grade_point)
        elif score >= 70:
            grade_point = 2.2
            per_score = (2.7 - 2.2) / (75 - 70)
            grade_point += (score - 70) * per_score
            grade_point = float('%.2f' % grade_point)
        elif score >= 65:
            grade_point = 1.7
            per_score = (2.2 - 1.7) / (70 - 65)
            grade_point += (score - 65) * per_score
            grade_point = float('%.2f' % grade_point)
        elif score >= 60:
            grade_point = 1.0
            per_score = (2 - 1.0) / (65 - 60)
            grade_point += (score - 60) * per_score
            grade_point = float('%.2f' % grade_point)
        # elif score >= 61:
        #     grade_point = 1.3
        #     per_score = (1.7 - 1.3) / (63 - 61)
        #     grade_point += (score - 61) * per_score
        #     grade_point = float('%.2f' % grade_point)
        # elif score == 60:
        #     grade_point = 1
        else:
            grade_point = 0
        return grade_point

    # 川大绩点计算
    def scdx_get_data(self, limit, score_list):
        score_sum = 0
        total_xuefen = 0
        total_count = 0
        for score in score_list:
            if limit not in score.xuanxiu:
                try:
                    score_sum += int(score.score) * float(score.xuefen)
                    total_xuefen += score.xuefen
                    total_count += 1
                except Exception as e:
                    log(e)
        avg_score = score_sum / total_xuefen
        grade_point = self.scdx_score_to_jidian(avg_score)
        data = {
            'avg_score': float('%.2f' % avg_score),
            'total_xuefen': total_xuefen,
            'grade_point': grade_point,
            'total_count': total_count
        }
        return data

    def scdx_counter(self, req):
        drop_elective_course = req['drop_elective_course'] if req['drop_elective_course'] else ''
        drop_limited_course = req['drop_limited_course'] if req['drop_limited_course'] else ''
        terms = req['terms'] if req['terms'] else ''
        uid = req['uid']
        score_list = []
        for term in terms:
            scores = UserScore.query.filter_by(xueqi=term, uid=int(uid)).all()
            for score in scores:
                score_list.append(score)
        if drop_elective_course and not drop_limited_course:
            data = self.scdx_get_data('选', score_list)
            return data
        elif drop_limited_course and not drop_elective_course:
            data = self.scdx_get_data('限', score_list)
            return data
        elif drop_elective_course and drop_limited_course:
            score_sum = 0
            total_xuefen = 0
            total_count = 0
            for score in score_list:
                if '限' not in score.xuanxiu and '选' not in score.xuanxiu:
                    try:
                        score_sum += int(score.score) * float(score.xuefen)
                        total_xuefen += score.xuefen
                        total_count += 1
                    except Exception as e:
                        log(e)
            avg_score = score_sum / total_xuefen
            grade_point = self.scdx_score_to_jidian(avg_score)
            data = {
                'avg_score': float('%.2f' % avg_score),
                'total_xuefen': total_xuefen,
                'grade_point': grade_point,
                'total_count': total_count
            }
            return data
        else:
            score_sum = 0
            total_xuefen = 0
            total_count = 0
            for score in score_list:
                try:
                    score_sum += int(score.score) * float(score.xuefen)
                    total_xuefen += score.xuefen
                    total_count += 1
                except Exception as e:
                    log(e)
            avg_score = score_sum / total_xuefen
            grade_point = self.scdx_score_to_jidian(avg_score)
            data = {
                'avg_score': float('%.2f' % avg_score),
                'total_xuefen': total_xuefen,
                'grade_point': grade_point,
                'total_count': total_count
            }
            return data

    def scsd_counter(self, req):
        drop_elective_course = req['drop_elective_course'] if req['drop_elective_course'] else ''
        drop_limited_course = req['drop_limited_course'] if req['drop_limited_course'] else ''
        terms = req['terms'] if req['terms'] else ''
        uid = req['uid']
        score_list = []
        for term in terms:
            scores = UserScore.query.filter_by(xueqi=term, uid=int(uid)).all()
            for score in scores:
                score_list.append(score)
        if drop_elective_course and not drop_limited_course:
            score_sum = 0
            total_xuefen = 0
            total_point = 0
            total_count = 0
            for score in score_list:
                if '选' not in score.xuanxiu:
                    try:
                        score_sum += float(score.score) * float(score.xuefen)
                        total_xuefen += score.xuefen
                        total_point += float(score.jidian) * float(score.xuefen)
                        total_count += 1
                    except Exception as e:
                        if score.score == '优':
                            score_sum += 90 * float(score.xuefen)
                        elif score.score == '良':
                            score_sum += 77 * float(score.xuefen)
                        elif score.score == '中':
                            score_sum += 67 * float(score.xuefen)
                        elif score.score == '及格':
                            score_sum += 60 * float(score.xuefen)
                        elif score.score == ('不及格' and ''):
                            score_sum += 0
                avg_score = score_sum / total_xuefen
            grade_point = total_point / total_xuefen
            data = {
                'avg_score': float('%.2f' % avg_score),
                'total_xuefen': total_xuefen,
                'grade_point': float('%.2f' % grade_point),
                'total_count': total_count
            }
            return data
        elif drop_limited_course and not drop_elective_course:
            score_sum = 0
            total_xuefen = 0
            total_point = 0
            total_count = 0
            for score in score_list:
                if '限' not in score.xuanxiu:
                    try:
                        score_sum += float(score.score) * float(score.xuefen)
                        total_xuefen += score.xuefen
                        total_point += float(score.jidian) * float(score.xuefen)
                        total_count += 1
                    except Exception as e:
                        if score.score == '优':
                            score_sum += 90 * float(score.xuefen)
                        elif score.score == '良':
                            score_sum += 77 * float(score.xuefen)
                        elif score.score == '中':
                            score_sum += 67 * float(score.xuefen)
                        elif score.score == '及格':
                            score_sum += 60 * float(score.xuefen)
                        elif score.score == ('不及格' and ''):
                            score_sum += 0
                avg_score = score_sum / total_xuefen
            grade_point = total_point / total_xuefen
            data = {
                'avg_score': float('%.2f' % avg_score),
                'total_xuefen': total_xuefen,
                'grade_point': float('%.2f' % grade_point),
                'total_count': total_count
            }
            return data
        elif drop_elective_course and drop_limited_course:
            score_sum = 0
            total_xuefen = 0
            total_point = 0
            total_count = 0
            for score in score_list:
                if '限' not in score.xuanxiu and '选' not in score.xuanxiu:
                    try:
                        score_sum += float(score.score) * float(score.xuefen)
                        total_xuefen += score.xuefen
                        total_point += float(score.jidian) * float(score.xuefen)
                        total_count += 1
                    except Exception as e:
                        if score.score == '优':
                            score_sum += 90 * float(score.xuefen)
                        elif score.score == '良':
                            score_sum += 77 * float(score.xuefen)
                        elif score.score == '中':
                            score_sum += 67 * float(score.xuefen)
                        elif score.score == '及格':
                            score_sum += 60 * float(score.xuefen)
                        elif score.score == ('不及格' and ''):
                            score_sum += 0
                avg_score = score_sum / total_xuefen
            grade_point = total_point / total_xuefen
            data = {
                'avg_score': float('%.2f' % avg_score),
                'total_xuefen': total_xuefen,
                'grade_point': float('%.2f' % grade_point),
                'total_count': total_count
            }
            return data
        else:
            score_sum = 0
            total_xuefen = 0
            total_point = 0
            total_count = 0
            for score in score_list:
                try:
                    score_sum += float(score.score) * float(score.xuefen)
                    total_xuefen += score.xuefen
                    total_point += float(score.jidian) * float(score.xuefen)
                    total_count += 1
                except Exception as e:
                    if score.score == '优':
                        score_sum += 90 * float(score.xuefen)
                    elif score.score == '良':
                        score_sum += 77 * float(score.xuefen)
                    elif score.score == '中':
                        score_sum += 67 * float(score.xuefen)
                    elif score.score == '及格':
                        score_sum += 60 * float(score.xuefen)
                    elif score.score == ('不及格' and ''):
                        score_sum += 0
            avg_score = score_sum / total_xuefen
            grade_point = total_point / total_xuefen
            data = {
                'avg_score': float('%.2f' % avg_score),
                'total_xuefen': total_xuefen,
                'grade_point': float('%.2f' % grade_point),
                'total_count': total_count
            }
            return data

    def xnjd_counter(self, req):
        drop_elective_course = req['drop_elective_course'] if req['drop_elective_course'] else ''
        drop_limited_course = req['drop_limited_course'] if req['drop_limited_course'] else ''
        terms = req['terms'] if req['terms'] else ''
        uid = req['uid']
        score_list = []
        for term in terms:
            scores = UserScore.query.filter_by(xueqi=term, uid=int(uid)).all()
            for score in scores:
                score_list.append(score)
        if drop_elective_course and not drop_limited_course:
            score_sum = 0
            total_xuefen = 0
            total_point = 0
            total_count = 0
            for score in score_list:
                if '选' not in score.xuanxiu:
                    try:
                        score_sum += float(score.score)
                        total_xuefen += score.xuefen
                        total_point += float(score.jidian) * float(score.xuefen)
                        total_count += 1
                    except Exception as e:
                        log(e)
            avg_score = score_sum / total_count
            grade_point = total_point / total_xuefen
            data = {
                'avg_score': float('%.2f' % avg_score),
                'total_xuefen': total_xuefen,
                'grade_point': float('%.2f' % grade_point),
                'total_count': total_count
            }
            return data
        elif drop_limited_course and not drop_elective_course:
            score_sum = 0
            total_xuefen = 0
            total_point = 0
            total_count = 0
            for score in score_list:
                if '限' not in score.xuanxiu:
                    try:
                        score_sum += float(score.score)
                        total_xuefen += score.xuefen
                        total_point += float(score.jidian) * float(score.xuefen)
                        total_count += 1
                    except Exception as e:
                        log(e)
            avg_score = score_sum / total_count
            grade_point = total_point / total_xuefen
            data = {
                'avg_score': float('%.2f' % avg_score),
                'total_xuefen': total_xuefen,
                'grade_point': float('%.2f' % grade_point),
                'total_count': total_count
            }
            return data
        elif drop_elective_course and drop_limited_course:
            score_sum = 0
            total_xuefen = 0
            total_point = 0
            total_count = 0
            for score in score_list:
                if '限' not in score.xuanxiu and '选' not in score.xuanxiu:
                    try:
                        score_sum += float(score.score)
                        total_xuefen += score.xuefen
                        total_point += float(score.jidian) * float(score.xuefen)
                        total_count += 1
                    except Exception as e:
                        log(e)
            avg_score = score_sum / total_count
            grade_point = total_point / total_xuefen
            data = {
                'avg_score': float('%.2f' % avg_score),
                'total_xuefen': total_xuefen,
                'grade_point': float('%.2f' % grade_point),
                'total_count': total_count
            }
            return data
        else:
            score_sum = 0
            total_xuefen = 0
            total_point = 0
            total_count = 0
            for score in score_list:
                try:
                    score_sum += float(score.score)
                    total_xuefen += score.xuefen
                    total_point += float(score.jidian) * float(score.xuefen)
                    total_count += 1
                except Exception as e:
                    log(e)
            avg_score = score_sum / total_count
            grade_point = total_point / total_xuefen
            data = {
                'avg_score': float('%.2f' % avg_score),
                'total_xuefen': total_xuefen,
                'grade_point': float('%.2f' % grade_point),
                'total_count': total_count
            }
            return data

    def main(self, college, req):
        if college == "四川大学":
            data = self.scdx_counter(req)
            return data
        if college == "四川师范大学":
            data = self.scsd_counter(req)
            return data
        if college == "西南交通大学":
            data = self.xnjd_counter(req)
            return data

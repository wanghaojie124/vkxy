from app.models.user_schedule import UserSchedule
from utils import log, black_list


class ScheduleController:

    def xnjd_schedule(self, uid):
        res_list = UserSchedule.query.filter_by(uid=uid).all()
        result = []
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
            result.append(res_dict)
        return result

    def main(self, college, uid):
        if college == '西南交通大学':
            data = self.xnjd_schedule(uid)
            return data
        elif college == '成都工业大学':
            pass
        else:
            info = {
                'status': 404,
                'msg': '需要参数college'
            }
            return info
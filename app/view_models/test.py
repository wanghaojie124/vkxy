import datetime
import re

ex = {'create_at': datetime.datetime(2019, 11, 14, 10, 31, 22), 'xh': 2017114242, 'name': '蔡良 ', 'jie': '1',
      'Mon': ['地球科学概论', '1-17周', 'X2337', '（汤家法）',
              ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17']],
      'Tues': '', 'Wed': '',
      'Thur': ['城市规划原理', '1-17周', 'X8524', '（陈蛟）',
                                      ['1', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15',
                                       '16', '17']],
      'Fri': ['数字图像处理', '1-17周', 'X4158', '（蔡国林）',
                                                             ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
                                                              '12', '13', '14', '15', '16', '17']], 'Sat': '',
      'Sun': ''}


def get_request_schedule(res, request_week):
    pop_list = []
    for k, v in res.items():
        if isinstance(v, list):
            if str(request_week) not in v[4]:
                pop_list.append(k)
    for i in pop_list:
        res.pop(i)
    return res

get_request_schedule(ex, 2)
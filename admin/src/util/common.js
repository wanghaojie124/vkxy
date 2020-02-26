import axios from 'axios'

export default {
    // 请求封装（json）
    requestData(_url, _method, _data) {
        return new Promise((resolve, reject) => {
            axios({
                method: _method,
                headers: {
                    'Content-type': 'application/json'
                },
                url: _url,
                data: _data
            }).then((response) => {
                resolve(response)
            }).catch((error) => {
                reject(error)
            })
        })
    },

    // 请求封装（params）
    requestDataParams(_url, _method, _data) {
        return new Promise((resolve, reject) => {
            axios({
                method: _method,
                headers: {
                    'Content-type': 'application/json'
                },
                url: _url,
                params: _data
            }).then((response) => {
                resolve(response)
            }).catch((error) => {
                reject(error)
            })
        })
    },

    // 请求封装（form-data）
    requestDataFile(_url, _method, _data) {
        let formData = new FormData(); // 创建一个form对象
        for (let i in _data) {
            formData.append(i, _data[i]);
        }

        return new Promise((resolve, reject) => {
            axios({
                method: _method,
                headers: {
                    'Content-type': 'multipart/form-data'
                },
                url: _url,
                data: formData
            }).then((response) => {
                resolve(response)
            }).catch((error) => {
                reject(error)
            })
        })
    },

    // 清空登录信息并登录
    loginOut(self) {
        localStorage.removeItem('timeStamp');
        localStorage.removeItem('islogin');
        self.$router.push({path: '/login'}); // 登录
    },

    // 学校列表
    collegeList() {
        return [{
            value: '西南交通大学',
            label: '西南交通大学'
        }, {
            value: '四川师范大学',
            label: '四川师范大学'
        }, {
            value: '四川大学',
            label: '四川大学'
        }, {
            value: '电子科技大学',
            label: '电子科技大学'
        }, {
            value: '成都理工大学',
            label: '成都理工大学'
        }
    ]
    }
}

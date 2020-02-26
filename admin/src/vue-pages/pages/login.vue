<template>
    <div class="login-bg">
        <div class="login">
            <div class="login-block">
                <div class="login-left">
                    <span>WELCOME</span>
                </div>
                <div class="login-right">
                    <div class="login-box">
                        <span>登陆</span>
                        <el-form label-position="left">
                            <el-form-item label="账号" label-width="60px">
                                <el-input v-model="username" placeholder="请输入账号" @keyup.enter.native="adminLogin()"></el-input>
                            </el-form-item>
                            <el-form-item label="密码" label-width="60px">
                                <el-input type="password" v-model="password" placeholder="请输入密码" @keyup.enter.native="adminLogin()"></el-input>
                            </el-form-item>
                        </el-form>
                        <div class="search-btn">
                            <el-button type="primary" :loading="loginLoading" size="medium" round @click="adminLogin()">登 陆</el-button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'login',
        data() {
            return {
                username: '', // 帐号
                password: '', // 密码
                loginLoading: false // 登录加载
            }
        },
        mounted() {

        },
        methods: {
            // 登陆
            adminLogin: function () {
                let self = this;

                if (this.checkUserName() && this.checkPassWord()) {
                    this.loginLoading = true;
                    this.common.requestDataFile('/vk/login', 'POST', {
                        username: self.username,
                        password: self.password
                    }).then((response) => {
                        var code = response.data.code;
                        if (code !== '404') {
                            self.$message({
                                message: '登陆成功',
                                type: 'success'
                            });
                            localStorage.timeStamp = JSON.stringify(new Date().getTime()); // 时间戳
                            localStorage.islogin = 'true'; // 登录状态
                            self.$router.push({path: '/home'}); // 首页
                        } else {
                            self.$message.error(response.data.msg);
                        }
                        self.loginLoading = false;
                    }).catch((error) => {
                        console.log(error);
                    })
                }
            },

            // 校验用户名
            checkUserName: function () {
                let username = this.username;

                if (username === '' || username === null || username === undefined) {
                    this.$message.error('用户名不能为空');
                    return false;
                } else {
                    return true;
                }
            },

            // 校验密码
            checkPassWord: function () {
                let password = this.password;

                if (password === '' || password === null || password === undefined) {
                    this.$message.error('密码不能为空');
                    return false;
                } else {
                    return true;
                }
            }
        }
    }
</script>

<style scoped>
    .login {
        height: 100%;
        background-color: rgba(107, 104, 122, 0.6);
        display: flex;
    }

    .login-block {
        margin: auto;
        background-color: #ffffff;
        width: 700px;
        height: 500px;
        display: flex;
    }

    .login-left {
        width: 230px;
        background-image: url("../../assets/img/login_left.png");
        background-size: cover;
    }

    .login-left span {
        display: block;
        text-align: center;
        margin-top: 80px;
        color: #ffffff;
        font-size: 20px;
    }

    .login-right {
        width: 470px;
    }

    .login-box {
        padding: 55px;
    }

    .login-right span {
        display: block;
        font-size: 20px;
        color: #666666;
        margin-top: 22px;
    }

    .search-btn {
        margin-top: 60px;
        text-align: right;
    }

    .code-img {
        position: absolute;
        top: 0;
        right: 0;
        height: 40px;
        width: 100px;
        cursor: pointer;
    }
</style>

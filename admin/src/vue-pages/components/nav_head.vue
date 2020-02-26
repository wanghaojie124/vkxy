<template>
    <div class="nav-head">
        <div class="logo"><img src="../../assets/img/login.png"/></div>
        <span class="name">欢迎进入微控校园后台管理系统</span>
        <span class="login-out" @click="signOut()">退出</span>
    </div>
</template>

<script>
    export default {
        name: 'nav_head',
        data() {
            return {}
        },
        methods: {
            // 退出
            signOut: function () {
                this.common.loginOut(this);
            }
        }
    }
</script>

<style scoped>
    .nav-head {
        display: flex;
    }

    .logo {
        width: 200px;
        height: 60px;
        font-size: 16px;
        text-align: center;
        color: #ffffff;
        padding: 10px 0;
    }

    .logo img {
        height: 100%;
    }

    .name {
        font-size: 14px;
        padding: 0 20px;
        color: #4176FF;
    }

    .login-out {
        position: absolute;
        right: 35px;
        cursor: pointer;
        color: #4176FF;
        border: 1px solid #4176FF;
        height: 25px;
        line-height: 25px;
        width: 45px;
        text-align: center;
        top: 15px;
        transition: all .3s ease;
    }

    .login-out:hover {
        color: #ffffff;
        background-color: #4176FF;
    }
</style>

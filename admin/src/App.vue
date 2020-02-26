<!--index.html的替代入口-->
<template>
    <div id="app">
        <router-view></router-view>
    </div>
</template>

<script>
    export default {
        name: 'App',
        data() {
            return {}
        },
        mounted() {
            // 登陆过期处理
            this.landingOverdue();
        },
        methods: {
            // 登陆过期处理
            landingOverdue: function () {
                if (localStorage.getItem('timeStamp')) {
                    var timeStamp = parseInt(localStorage.getItem('timeStamp')); // 获取缓存中时间戳
                    var nowTime = new Date().getTime(); // 当前时间戳
                    var exp = 12 * 60 * 60 * 1000; // 12个小时过期时间
                    if (nowTime - timeStamp > exp) {
                        // 清空用户登录信息
                        localStorage.removeItem('timeStamp');
                        localStorage.removeItem('islogin');
                        this.$message({
                            message: '登陆过期',
                            type: 'error'
                        });
                    }
                }
            }
        }
    }
</script>

<style>
    @import '../src/assets/style.css';

    #app {
        height: 100%;
    }
</style>

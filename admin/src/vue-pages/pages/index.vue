<template>
    <div class="index">
        <el-container>

            <!--头部导航-->
            <el-header>
                <nav-head></nav-head>
            </el-header>

            <el-container>

                <!--侧边导航-->
                <el-aside>
                    <nav-side></nav-side>
                </el-aside>

                <!--主内容-->
                <el-main>
                    <!--二级路由-->
                    <router-view></router-view>
                </el-main>

            </el-container>
        </el-container>
    </div>
</template>

<script>
    import navHead from '../components/nav_head'
    import navSide from '../components/nav_side'

    export default {
        name: 'index',
        data() {
            return {}
        },
        components: {
            navHead,
            navSide
        }
    }
</script>

<style>
    .index {
        height: 100%;
    }
</style>

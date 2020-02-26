<template>
    <div>
        <el-menu
            :default-active="active"
            :unique-opened="true"
            @select="handleSelect">
            <el-menu-item index="1">
                <div class="active"></div>
                <i class="iconfont icon-user"></i>
                <span slot="title">用户列表</span>
            </el-menu-item>
            <el-menu-item index="2">
                <div class="active"></div>
                <i class="iconfont icon-add-sale"></i>
                <span slot="title">资讯列表</span>
            </el-menu-item>
            <el-menu-item index="3">
                <div class="active"></div>
                <i class="iconfont icon-total"></i>
                <span slot="title">banner列表</span>
            </el-menu-item>
        </el-menu>
    </div>
</template>

<script>
    export default {
        name: 'nav_side',
        data() {
            return {
                active: '1' // 默认选中
            }
        },
        mounted() {
            // 刷新缓存选中
            this.defaultActive()
        },
        methods: {
            // 刷新缓存选中
            defaultActive() {
                const active = sessionStorage.getItem('active');
                if (active) {
                    this.active = active
                }
            },

            // 菜单选择
            handleSelect(key, keyPath) {
                switch (key) {
                    case '1':
                        this.$router.push({path: '/'});
                        break;
                    case '2':
                        this.$router.push({path: '/information'});
                        break;
                    case '3':
                        this.$router.push({path: '/banner'});
                        break;
                    default:
                        break
                }

                // 缓存选中
                sessionStorage.setItem('active', key)
            }
        }
    }
</script>

<style scoped>
</style>

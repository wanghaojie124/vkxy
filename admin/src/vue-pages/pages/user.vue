<template>
    <div class="user">
        <!--头部-->
        <div ref="headerView">
            <el-row>
                <el-col :span="24">
                    用户列表
                    <div class="el-header-right">
                        <el-button size="mini" type="primary" icon="el-icon-refresh" @click="refresh()"></el-button>
                    </div>
                </el-col>
            </el-row>
        </div>
        <!--筛选-->
        <div ref="headSearchView">
            <el-row class="el-top">
                <el-col :span="24">
                    <el-select v-model="college" clearable size="small" placeholder="学校">
                        <el-option
                            v-for="item in collegeList"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                        </el-option>
                    </el-select>
                    <el-button size="small" type="primary" icon="el-icon-search" @click="refresh()">查询</el-button>
                </el-col>
            </el-row>
        </div>
        <!--主内容-->
        <el-table
            v-loading="loading"
            class="el-top"
            :data="userList"
            :height="fullHeight || null"
            size="small">
            <el-table-column prop="id" label="id">
            </el-table-column>
            <el-table-column prop="name" label="姓名">
            </el-table-column>
            <el-table-column prop="username" label="账号">
            </el-table-column>
            <el-table-column prop="password" label="密码">
            </el-table-column>
            <el-table-column prop="phone_number" label="手机号">
            </el-table-column>
        </el-table>
        <!--分页-->
        <el-row>
            <el-col :md="24" class="page-block">
                <el-pagination
                    :background="true"
                    :page-size="userPageSize"
                    :total="userTotal"
                    :current-page="userCurrentPage"
                    layout="total, prev, pager, next, jumper"
                    @current-change="userCurrentChange">
                </el-pagination>
            </el-col>
        </el-row>
    </div>
</template>

<script>
    export default {
        name: 'user',
        data() {
            return {
                token: '', // 登录凭证
                fullHeight: 0, // 窗口高度

                collegeList: this.common.collegeList(),
                college: '', // 学校

                loading: true, // 加载状态
                userList: [], // 用户列表
                userCurrentPage: 1, // 当前页数
                userPageSize: 20, // 每页显示条目个数
                userTotal: 0 // 总条目数
            }
        },
        mounted() {
            this.fullHeight = document.documentElement.clientHeight - this.$refs.headerView.offsetHeight - this.$refs.headSearchView.offsetHeight - 220;
            window.onresize = () => {
                this.fullHeight = document.documentElement.clientHeight - this.$refs.headerView.offsetHeight - this.$refs.headSearchView.offsetHeight - 220;
            };
            if (localStorage.getItem('islogin')) {
                // 获取用户列表
                this.getUserList();
            } else {
                this.common.loginOut(this);
            }
        },
        methods: {
            // 获取用户列表
            getUserList: function () {
                var self = this;
                this.loading = true;

                this.common.requestDataParams('/vk/users', 'GET', {
                    college: self.college,
                    page: self.userCurrentPage,
                    limit: self.userPageSize
                }).then((response) => {
                    self.userList = response.data.data;
                    self.userTotal = response.data.total;
                    self.loading = false;
                }).catch((error) => {
                    console.log(error);
                })
            },

            // 切换用户列表分页
            userCurrentChange: function (e) {
                this.userCurrentPage = e;
                // 获取用户列表
                this.getUserList();
            },

            // 刷新
            refresh: function () {
                // 获取用户列表
                this.getUserList();
            }
        }
    }
</script>

<style scoped>
</style>

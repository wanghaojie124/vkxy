<template>
    <div class="information">
        <!--头部-->
        <div ref="headerView">
            <el-row>
                <el-col :span="24">
                    资讯列表
                    <div class="el-header-right">
                        <el-button size="mini" type="primary" @click="addInformationDialog = true">新增资讯</el-button>
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
            :data="informationList"
            :height="fullHeight || null"
            size="small">
            <el-table-column prop="title" label="标题">
            </el-table-column>
            <el-table-column prop="intro" label="简介">
            </el-table-column>
            <el-table-column prop="weight" label="权重">
            </el-table-column>
            <el-table-column prop="on_index" label="首页显示">
                <template slot-scope="scope">
                    <div v-if="scope.row.on_index === 0" class="red-text">否</div>
                    <div v-else class="green-text">是</div>
                </template>
            </el-table-column>
            <el-table-column prop="type" label="类型">
            </el-table-column>
            <el-table-column prop="link" label="链接">
            </el-table-column>
            <el-table-column label="图片" width="200">
                <template slot-scope="scope">
                    <img class="information-img" :src="scope.row.image"/>
                </template>
            </el-table-column>
            <el-table-column prop="content" label="内容">
            </el-table-column>
            <el-table-column prop="college" label="学校">
            </el-table-column>
            <el-table-column fixed="right" label="操作" width="150">
                <template slot-scope="scope">
                    <el-button size="mini" type="primary" @click="editInformation(scope.row)">编辑</el-button>
                    <el-button size="mini" type="danger" @click="deleteInformation(scope.row)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
        <!--分页-->
        <el-row>
            <el-col :md="24" class="page-block">
                <el-pagination
                    :background="true"
                    :page-size="informationPageSize"
                    :total="informationTotal"
                    :current-page="informationCurrentPage"
                    layout="total, prev, pager, next, jumper"
                    @current-change="informationCurrentChange">
                </el-pagination>
            </el-col>
        </el-row>

        <!--新增资讯-->
        <el-dialog title="新增资讯" :visible.sync="addInformationDialog" :close-on-click-modal="false" width="500px">
            <el-form @submit.native.prevent>
                <el-form-item label="标题 *" size="medium" label-width="100px">
                    <el-input v-model="informationTitle"></el-input>
                </el-form-item>
                <el-form-item label="简介" size="medium" label-width="100px">
                    <el-input v-model="informationIntro"></el-input>
                </el-form-item>
                <el-form-item label="内容" size="medium" label-width="100px">
                    <el-input v-model="informationContent"></el-input>
                </el-form-item>
                <el-form-item label="权重 *" size="medium" label-width="100px">
                    <el-input v-model="informationWeight" type="number" placeholder="数值越大，在首页显示越靠前"></el-input>
                </el-form-item>
                <el-form-item label="学校" size="medium" label-width="100px">
                    <el-select v-model="informationCollege" size="medium">
                        <el-option
                            v-for="item in collegeList"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="公告栏显示" size="medium" label-width="100px">
                    <el-select v-model="informationOnIndex" size="medium">
                        <el-option
                            v-for="item in noticeList"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="类型 *" size="medium" label-width="100px">
                    <el-input v-model="informationType"></el-input>
                </el-form-item>
                <el-form-item label="链接 *" size="medium" label-width="100px">
                    <el-input v-model="informationLink"></el-input>
                </el-form-item>
                <el-form-item label="图片 *" size="medium" label-width="100px">
                    <div class="file-creation">
                        <el-button size="small" type="primary">选择文章图片</el-button>
                        <input ref="clearImageFile" type="file" accept="image/*" @change="selectImage($event)">
                    </div>
                    <div class="el-top">
                        <img class="file-image" :src="informationImage">
                    </div>
                </el-form-item>
            </el-form>
            <div slot="footer">
                <el-button size="small" @click="addInformationDialog = false">取 消</el-button>
                <el-button size="small" type="primary" :loading="addInformationSureLoad" @click="addInformationSure()">确 定</el-button>
            </div>
        </el-dialog>

        <!--编辑资讯-->
        <el-dialog title="编辑资讯" :visible.sync="editInformationDialog" :close-on-click-modal="false" width="500px">
            <el-form @submit.native.prevent>
                <el-form-item label="标题 *" size="medium" label-width="100px">
                    <el-input v-model="editInformationTitle"></el-input>
                </el-form-item>
                <el-form-item label="简介" size="medium" label-width="100px">
                    <el-input v-model="editInformationIntro"></el-input>
                </el-form-item>
                <el-form-item label="内容" size="medium" label-width="100px">
                    <el-input v-model="editInformationContent"></el-input>
                </el-form-item>
                <el-form-item label="权重 *" size="medium" label-width="100px">
                    <el-input v-model="editInformationWeight" type="number" placeholder="数值越大，在首页显示越靠前"></el-input>
                </el-form-item>
                <el-form-item label="学校" size="medium" label-width="100px">
                    <el-select v-model="editInformationCollege" size="medium">
                        <el-option
                            v-for="item in collegeList"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="公告栏显示" size="medium" label-width="100px">
                    <el-select v-model="editInformationOnIndex" size="medium">
                        <el-option
                            v-for="item in noticeList"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="类型 *" size="medium" label-width="100px">
                    <el-input v-model="editInformationType"></el-input>
                </el-form-item>
                <el-form-item label="链接 *" size="medium" label-width="100px">
                    <el-input v-model="editInformationLink"></el-input>
                </el-form-item>
                <el-form-item label="图片 *" size="medium" label-width="100px">
                    <div class="file-creation">
                        <el-button size="small" type="primary">选择文章图片</el-button>
                        <input ref="clearImageFile1" type="file" accept="image/*" @change="selectImage1($event)">
                    </div>
                    <div class="el-top">
                        <img class="file-image" :src="editInformationImage">
                    </div>
                </el-form-item>
            </el-form>
            <div slot="footer">
                <el-button size="small" @click="editInformationDialog = false">取 消</el-button>
                <el-button size="small" type="primary" :loading="editInformationSureLoad" @click="editInformationSure()">确 定</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
    export default {
        name: 'information',
        data() {
            return {
                token: '', // 登录凭证
                fullHeight: 0, // 窗口高度

                collegeList: this.common.collegeList(),
                college: '', // 学校

                loading: true, // 加载状态
                informationList: [], // 资讯列表
                informationCurrentPage: 1, // 当前页数
                informationPageSize: 20, // 每页显示条目个数
                informationTotal: 0, // 总条目数

                addInformationDialog: false, // 新增资讯窗口
                addInformationSureLoad: false, // 加载
                noticeList: [{
                    value: 0,
                    label: '不显示'
                }, {
                    value: 1,
                    label: '显示'
                }],
                informationTitle: '', // 标题
                informationIntro: '', // 简介
                informationContent: '', // 内容
                informationWeight: '', // 权重
                informationCollege: '西南交通大学', // 学校
                informationOnIndex: 0, // 公告栏显示
                informationType: '', // 类型
                informationLink: '', // 链接
                informationImage: '', // 图片

                editInformationDialog: false, // 编辑资讯窗口
                editInformationSureLoad: false, // 加载
                editInformationId: '', // 当前编辑的ID
                editInformationTitle: '', // 标题
                editInformationIntro: '', // 简介
                editInformationContent: '', // 内容
                editInformationWeight: '', // 权重
                editInformationCollege: '西南交通大学', // 学校
                editInformationOnIndex: '', // 公告栏显示
                editInformationType: '', // 类型
                editInformationLink: '', // 链接
                editInformationImage: '' // 图片
            }
        },
        mounted() {
            this.fullHeight = document.documentElement.clientHeight - this.$refs.headerView.offsetHeight - this.$refs.headSearchView.offsetHeight - 220;
            window.onresize = () => {
                this.fullHeight = document.documentElement.clientHeight - this.$refs.headerView.offsetHeight - this.$refs.headSearchView.offsetHeight - 220;
            };
            if (localStorage.getItem('islogin')) {
                // 获取资讯列表
                this.getInformationList();
            } else {
                this.common.loginOut(this);
            }
        },
        methods: {
            // 获取资讯列表
            getInformationList: function () {
                var self = this;
                this.loading = true;

                this.common.requestDataParams('/vk/articlelist', 'GET', {
                    college: self.college,
                    page: self.informationCurrentPage,
                    limit: self.informationPageSize
                }).then((response) => {
                    self.informationList = response.data.data;
                    self.informationTotal = response.data.total;
                    self.loading = false;
                }).catch((error) => {
                    console.log(error);
                })
            },

            // 新增资讯
            addInformationSure: function () {
                var self = this;

                if (this.checkAddInformation()) {
                    this.addInformationSureLoad = true;
                    const file = this.$refs.clearImageFile.files[0];
                    this.common.requestDataFile('/vk/addarticle', 'POST', {
                        title: self.informationTitle,
                        intro: self.informationIntro,
                        content: self.informationContent,
                        weight: self.informationWeight,
                        college: self.informationCollege,
                        on_index: self.informationOnIndex,
                        type: self.informationType,
                        link: self.informationLink,
                        image: file
                    }).then((response) => {
                        self.addInformationDialog = false;
                        self.addInformationSureLoad = false;
                        self.informationTitle = '';
                        self.informationIntro = '';
                        self.informationContent = '';
                        self.informationWeight = '';
                        self.informationCollege = '西南交通大学';
                        self.informationOnIndex = 0;
                        self.informationType = '';
                        self.informationLink = '';
                        self.informationImage = '';
                        self.$refs.clearImageFile.value = '';
                        // 获取资讯列表
                        self.getInformationList();
                    }).catch((error) => {
                        console.log(error);
                    })
                }
            },

            // 校验新增资讯
            checkAddInformation: function () {
                let informationTitle = this.informationTitle;
                let informationWeight = this.informationWeight;
                let informationType = this.informationType;
                let informationLink = this.informationLink;
                let informationImage = this.$refs.clearImageFile.value;

                if (informationTitle === '' || informationTitle === null || informationTitle === undefined) {
                    this.$message.error('标题不能为空');
                    return false;
                } else if (informationWeight === '' || informationWeight === null || informationWeight === undefined) {
                    this.$message.error('权重不能为空');
                    return false;
                } else if (informationType === '' || informationType === null || informationType === undefined) {
                    this.$message.error('类型不能为空');
                    return false;
                } else if (informationLink === '' || informationLink === null || informationLink === undefined) {
                    this.$message.error('链接不能为空');
                    return false;
                } else if (informationImage === '' || informationImage === null || informationImage === undefined) {
                    this.$message.error('图片不能为空');
                    return false;
                } else {
                    return true;
                }
            },

            // 选择文章图片
            selectImage: function (e) {
                const file = e.target.files[0];
                if (file) {
                    this.informationImage = window.URL.createObjectURL(file)
                } else {
                    this.$refs.clearImageFile.value = '';
                    this.informationImage = ''
                }
            },

            // 编辑资讯窗口
            editInformation: function (e) {
                this.editInformationDialog = true;
                this.editInformationId = e.id;
                this.editInformationTitle = e.title;
                this.editInformationIntro = e.intro;
                this.editInformationContent = e.content;
                this.editInformationWeight = e.weight;
                this.editInformationCollege = e.college;
                this.editInformationOnIndex = e.on_index;
                this.editInformationType = e.type;
                this.editInformationLink = e.link;
                this.editInformationImage = e.image;
            },

            // 编辑资讯
            editInformationSure: function () {
                var self = this;

                if (this.checkEditInformation()) {
                    this.editInformationSureLoad = true;
                    const file = this.$refs.clearImageFile1.files[0];
                    this.common.requestDataFile('/vk/updatearticles', 'POST', {
                        id: self.editInformationId,
                        title: self.editInformationTitle,
                        intro: self.editInformationIntro,
                        content: self.editInformationContent,
                        weight: self.editInformationWeight,
                        college: self.editInformationCollege,
                        on_index: self.editInformationOnIndex,
                        type: self.editInformationType,
                        link: self.editInformationLink,
                        image: file ? file : '',
                        status: 1
                    }).then((response) => {
                        self.editInformationDialog = false;
                        self.editInformationSureLoad = false;
                        self.$refs.clearImageFile1.value = '';
                        // 获取资讯列表
                        self.getInformationList();
                    }).catch((error) => {
                        console.log(error);
                    })
                }
            },

            // 校验编辑资讯
            checkEditInformation: function () {
                let editInformationTitle = this.editInformationTitle;
                let editInformationWeight = this.editInformationWeight;
                let editInformationType = this.editInformationType;
                let editInformationLink = this.editInformationLink;

                if (editInformationTitle === '' || editInformationTitle === null || editInformationTitle === undefined) {
                    this.$message.error('标题不能为空');
                    return false;
                } else if (editInformationWeight === '' || editInformationWeight === null || editInformationWeight === undefined) {
                    this.$message.error('权重不能为空');
                    return false;
                } else if (editInformationType === '' || editInformationType === null || editInformationType === undefined) {
                    this.$message.error('类型不能为空');
                    return false;
                } else if (editInformationLink === '' || editInformationLink === null || editInformationLink === undefined) {
                    this.$message.error('链接不能为空');
                    return false;
                } else {
                    return true;
                }
            },

            // 选择文章图片
            selectImage1: function (e) {
                const file = e.target.files[0];
                if (file) {
                    this.editInformationImage = window.URL.createObjectURL(file)
                } else {
                    this.$refs.clearImageFile1.value = '';
                    this.editInformationImage = ''
                }
            },

            // 删除资讯
            deleteInformation: function (e) {
                var self = this;

                this.$confirm('是否删除？', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    self.common.requestDataFile('/vk/updatearticles', 'POST', {
                        id: e.id,
                        status: 0
                    }).then((response) => {
                        self.$message.success('删除成功');
                        // 获取资讯列表
                        self.getInformationList();
                    }).catch((error) => {
                        console.log(error);
                    })
                }).catch((error) => {
                    console.log(error);
                })
            },

            // 切换资讯列表分页
            informationCurrentChange: function (e) {
                this.informationCurrentPage = e;
                // 获取资讯列表
                this.getInformationList();
            },

            // 刷新
            refresh: function () {
                // 获取资讯列表
                this.getInformationList();
            }
        }
    }
</script>

<style scoped>
    .information-img {
        width: 100%;
        display: block;
    }

    .file-creation {
        position: relative;
        display: inline-block;
    }

    .file-creation .el-button {
        display: block;
    }

    .file-creation:hover .el-button--primary {
        opacity: 0.8;
    }

    .file-creation input {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        opacity: 0;
        font-size: 0;
        cursor: pointer;
    }

    .file-image {
        width: 150px;
    }
</style>

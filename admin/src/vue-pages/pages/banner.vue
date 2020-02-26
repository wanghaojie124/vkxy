<template>
    <div class="banner">
        <!--头部-->
        <div ref="headerView">
            <el-row>
                <el-col :span="24">
                    banner列表
                    <div class="el-header-right">
                        <el-button size="mini" type="primary" @click="addBannerDialog = true">新增banner</el-button>
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
            :data="bannerList"
            :height="fullHeight || null"
            size="small">
            <el-table-column prop="title" label="标题">
            </el-table-column>
            <el-table-column prop="weight" label="权重">
            </el-table-column>
            <el-table-column label="今日特价显示" width="100">
                <template slot-scope="scope">
                    <div v-if="scope.row.special === 0" class="red-text">否</div>
                    <div v-else class="green-text">是</div>
                </template>
            </el-table-column>
            <el-table-column prop="mini" label="小程序ID">
            </el-table-column>
            <el-table-column prop="link" label="链接">
            </el-table-column>
            <el-table-column label="图片" width="200">
                <template slot-scope="scope">
                    <img class="banner-img" :src="scope.row.image"/>
                </template>
            </el-table-column>
            <el-table-column prop="college" label="大学">
            </el-table-column>
            <el-table-column prop="price" label="正价">
            </el-table-column>
            <el-table-column prop="bargain_price" label="折扣价">
            </el-table-column>
            <el-table-column fixed="right" label="操作" width="150">
                <template slot-scope="scope">
                    <el-button size="mini" type="primary" @click="editBanner(scope.row)">编辑</el-button>
                    <el-button size="mini" type="danger" @click="deleteBanner(scope.row)">删除</el-button>
                </template>
            </el-table-column>
        </el-table>
        <!--分页-->
        <el-row>
            <el-col :md="24" class="page-block">
                <el-pagination
                    :background="true"
                    :page-size="bannerPageSize"
                    :total="bannerTotal"
                    :current-page="bannerCurrentPage"
                    layout="total, prev, pager, next, jumper"
                    @current-change="bannerCurrentChange">
                </el-pagination>
            </el-col>
        </el-row>

        <!--新增banner-->
        <el-dialog title="新增banner" :visible.sync="addBannerDialog" :close-on-click-modal="false" width="500px">
            <el-form @submit.native.prevent>
                <el-form-item label="标题 *" size="medium" label-width="100px">
                    <el-input v-model="bannerTitle"></el-input>
                </el-form-item>
                <el-form-item label="权重 *" size="medium" label-width="100px">
                    <el-input v-model="bannerWeight" type="number" placeholder="数值越大，在首页显示越靠前"></el-input>
                </el-form-item>
                <el-form-item label="学校" size="medium" label-width="100px">
                    <el-select v-model="bannerCollege" size="medium">
                        <el-option
                            v-for="item in collegeList"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="今日特价显示" size="medium" label-width="100px">
                    <el-select v-model="bannerSpecial" size="medium">
                        <el-option
                            v-for="item in specialList"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="小程序ID" size="medium" label-width="100px">
                    <el-input v-model="bannerMini" placeholder="公众号链接可不填"></el-input>
                </el-form-item>
                <el-form-item label="链接 *" size="medium" label-width="100px">
                    <el-input v-model="bannerLink"></el-input>
                </el-form-item>
                <el-form-item label="正价 *" size="medium" label-width="100px">
                    <el-input v-model="bannerPrice" type="number"></el-input>
                </el-form-item>
                <el-form-item label="折扣价 *" size="medium" label-width="100px">
                    <el-input v-model="bannerBargainPrice" type="number"></el-input>
                </el-form-item>
                <el-form-item label="图片 *" size="medium" label-width="100px">
                    <div class="file-creation">
                        <el-button size="small" type="primary">选择banner图片</el-button>
                        <input ref="clearImageFile" type="file" accept="image/*" @change="selectImage($event)">
                    </div>
                    <div class="el-top">
                        <img class="file-image" :src="bannerImage">
                    </div>
                </el-form-item>
            </el-form>
            <div slot="footer">
                <el-button size="small" @click="addBannerDialog = false">取 消</el-button>
                <el-button size="small" type="primary" :loading="addBannerSureLoad" @click="addBannerSure()">确 定</el-button>
            </div>
        </el-dialog>

        <!--编辑banner-->
        <el-dialog title="编辑banner" :visible.sync="editBannerDialog" :close-on-click-modal="false" width="500px">
            <el-form @submit.native.prevent>
                <el-form-item label="标题 *" size="medium" label-width="100px">
                    <el-input v-model="editBannerTitle"></el-input>
                </el-form-item>
                <el-form-item label="权重 *" size="medium" label-width="100px">
                    <el-input v-model="editBannerWeight" type="number" placeholder="数值越大，在首页显示越靠前"></el-input>
                </el-form-item>
                <el-form-item label="学校" size="medium" label-width="100px">
                    <el-select v-model="editBannerCollege" size="medium">
                        <el-option
                            v-for="item in collegeList"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="今日特价显示" size="medium" label-width="100px">
                    <el-select v-model="editBannerSpecial" size="medium">
                        <el-option
                            v-for="item in specialList"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="小程序ID" size="medium" label-width="100px">
                    <el-input v-model="editBannerMini" placeholder="公众号链接可不填"></el-input>
                </el-form-item>
                <el-form-item label="链接 *" size="medium" label-width="100px">
                    <el-input v-model="editBannerLink"></el-input>
                </el-form-item>
                <el-form-item label="正价 *" size="medium" label-width="100px">
                    <el-input v-model="editBannerPrice" type="number"></el-input>
                </el-form-item>
                <el-form-item label="折扣价 *" size="medium" label-width="100px">
                    <el-input v-model="editBannerBargainPrice" type="number"></el-input>
                </el-form-item>
                <el-form-item label="图片 *" size="medium" label-width="100px">
                    <div class="file-creation">
                        <el-button size="small" type="primary">选择banner图片</el-button>
                        <input ref="clearImageFile1" type="file" accept="image/*" @change="selectImage1($event)">
                    </div>
                    <div class="el-top">
                        <img class="file-image" :src="editBannerImage">
                    </div>
                </el-form-item>
            </el-form>
            <div slot="footer">
                <el-button size="small" @click="editBannerDialog = false">取 消</el-button>
                <el-button size="small" type="primary" :loading="editBannerSureLoad" @click="editBannerSure()">确 定</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
    export default {
        name: 'banner',
        data() {
            return {
                token: '', // 登录凭证
                fullHeight: 0, // 窗口高度

                collegeList: this.common.collegeList(),
                college: '', // 学校

                loading: true, // 加载状态
                bannerList: [], // banner列表
                bannerCurrentPage: 1, // 当前页数
                bannerPageSize: 20, // 每页显示条目个数
                bannerTotal: 0, // 总条目数

                addBannerDialog: false, // 新增banner窗口
                addBannerSureLoad: false, // 加载
                specialList: [{
                    value: 0,
                    label: '不显示'
                }, {
                    value: 1,
                    label: '显示'
                }],
                bannerTitle: '', // 标题
                bannerWeight: '', // 权重
                bannerCollege: '西南交通大学', // 学校
                bannerSpecial: 0, // 今日特价显示
                bannerMini: '', // 小程序ID
                bannerLink: '', // 链接
                bannerPrice: '', // 正价
                bannerBargainPrice: '', // 折扣价
                bannerImage: '', // 图片

                editBannerDialog: false, // 编辑banner窗口
                editBannerSureLoad: false, // 加载
                editBannerId: '', // 当前编辑的ID
                editBannerTitle: '', // 标题
                editBannerWeight: '', // 权重
                editBannerCollege: '西南交通大学', // 学校
                editBannerSpecial: '', // 今日特价显示
                editBannerMini: '', // 小程序ID
                editBannerLink: '', // 链接
                editBannerPrice: '', // 正价
                editBannerBargainPrice: '', // 折扣价
                editBannerImage: '' // 图片
            }
        },
        mounted() {
            this.fullHeight = document.documentElement.clientHeight - this.$refs.headerView.offsetHeight - this.$refs.headSearchView.offsetHeight - 220;
            window.onresize = () => {
                this.fullHeight = document.documentElement.clientHeight - this.$refs.headerView.offsetHeight - this.$refs.headSearchView.offsetHeight - 220;
            };
            if (localStorage.getItem('islogin')) {
                // 获取banner列表
                this.getBannerList();
            } else {
                this.common.loginOut(this);
            }
        },
        methods: {
            // 获取banner列表
            getBannerList: function () {
                var self = this;
                this.loading = true;

                this.common.requestDataParams('/vk/bannerlist', 'GET', {
                    college: self.college,
                    page: self.bannerCurrentPage,
                    limit: self.bannerPageSize
                }).then((response) => {
                    self.bannerList = response.data.data;
                    self.bannerTotal = response.data.total;
                    self.loading = false;
                }).catch((error) => {
                    console.log(error);
                })
            },

            // 新增banner
            addBannerSure: function () {
                var self = this;

                if (this.checkAddBanner()) {
                    this.addBannerSureLoad = true;
                    const file = this.$refs.clearImageFile.files[0];
                    this.common.requestDataFile('/vk/addbanner', 'POST', {
                        title: self.bannerTitle,
                        weight: self.bannerWeight,
                        college: self.bannerCollege,
                        special: self.bannerSpecial,
                        mini: self.bannerMini,
                        link: self.bannerLink,
                        price: self.bannerPrice,
                        bargain_price: self.bannerBargainPrice,
                        image: file
                    }).then((response) => {
                        self.addBannerDialog = false;
                        self.addBannerSureLoad = false;
                        self.bannerTitle = '';
                        self.bannerWeight = '';
                        self.bannerCollege = '西南交通大学';
                        self.bannerSpecial = 0;
                        self.bannerMini = '';
                        self.bannerLink = '';
                        self.bannerPrice = '';
                        self.bannerBargainPrice = '';
                        self.bannerImage = '';
                        self.$refs.clearImageFile.value = '';
                        // 获取banner列表
                        self.getBannerList();
                    }).catch((error) => {
                        console.log(error);
                    })
                }
            },

            // 校验新增banner
            checkAddBanner: function () {
                let bannerTitle = this.bannerTitle;
                let bannerWeight = this.bannerWeight;
                let bannerLink = this.bannerLink;
                let bannerPrice = this.bannerPrice;
                let bannerBargainPrice = this.bannerBargainPrice;
                let bannerImage = this.$refs.clearImageFile.value;

                if (bannerTitle === '' || bannerTitle === null || bannerTitle === undefined) {
                    this.$message.error('标题不能为空');
                    return false;
                } else if (bannerWeight === '' || bannerWeight === null || bannerWeight === undefined) {
                    this.$message.error('权重不能为空');
                    return false;
                } else if (bannerLink === '' || bannerLink === null || bannerLink === undefined) {
                    this.$message.error('链接不能为空');
                    return false;
                } else if (bannerPrice === '' || bannerPrice === null || bannerPrice === undefined) {
                    this.$message.error('正价不能为空');
                    return false;
                } else if (bannerBargainPrice === '' || bannerBargainPrice === null || bannerBargainPrice === undefined) {
                    this.$message.error('折扣价不能为空');
                    return false;
                } else if (bannerImage === '' || bannerImage === null || bannerImage === undefined) {
                    this.$message.error('图片不能为空');
                    return false;
                } else {
                    return true;
                }
            },

            // 选择banner图片
            selectImage: function (e) {
                const file = e.target.files[0];
                if (file) {
                    this.bannerImage = window.URL.createObjectURL(file)
                } else {
                    this.$refs.clearImageFile.value = '';
                    this.bannerImage = ''
                }
            },

            // 编辑banner窗口
            editBanner: function (e) {
                this.editBannerDialog = true;
                this.editBannerId = e.id;
                this.editBannerTitle = e.title;
                this.editBannerWeight =  e.weight;
                this.editBannerCollege = e.college;
                this.editBannerSpecial = e.special;
                this.editBannerMini = e.mini;
                this.editBannerLink = e.link;
                this.editBannerPrice = e.price;
                this.editBannerBargainPrice = e.bargain_price;
                this.editBannerImage = e.image;
            },

            // 编辑banner
            editBannerSure: function () {
                var self = this;

                if (this.checkEditBanner()) {
                    this.editBannerSureLoad = true;
                    const file = this.$refs.clearImageFile1.files[0];
                    this.common.requestDataFile('/vk/updatebanners', 'POST', {
                        id: self.editBannerId,
                        title: self.editBannerTitle,
                        weight: self.editBannerWeight,
                        college: self.editBannerCollege,
                        special: self.editBannerSpecial,
                        mini: self.editBannerMini,
                        link: self.editBannerLink,
                        price: self.editBannerPrice,
                        bargain_price: self.editBannerBargainPrice,
                        image: file ? file : '',
                        status: 1
                    }).then((response) => {
                        self.editBannerDialog = false;
                        self.editBannerSureLoad = false;
                        self.$refs.clearImageFile1.value = '';
                        // 获取banner列表
                        this.getBannerList();
                    }).catch((error) => {
                        console.log(error);
                    })
                }
            },

            // 校验编辑banner
            checkEditBanner: function () {
                let editBannerTitle = this.editBannerTitle;
                let editBannerWeight = this.editBannerWeight;
                let editBannerLink = this.editBannerLink;
                let editBannerPrice = this.editBannerPrice;
                let editBannerBargainPrice = this.editBannerBargainPrice;

                if (editBannerTitle === '' || editBannerTitle === null || editBannerTitle === undefined) {
                    this.$message.error('标题不能为空');
                    return false;
                } else if (editBannerWeight === '' || editBannerWeight === null || editBannerWeight === undefined) {
                    this.$message.error('权重不能为空');
                    return false;
                } else if (editBannerLink === '' || editBannerLink === null || editBannerLink === undefined) {
                    this.$message.error('链接不能为空');
                    return false;
                } else if (editBannerPrice === '' || editBannerPrice === null || editBannerPrice === undefined) {
                    this.$message.error('正价不能为空');
                    return false;
                } else if (editBannerBargainPrice === '' || editBannerBargainPrice === null || editBannerBargainPrice === undefined) {
                    this.$message.error('折扣价不能为空');
                    return false;
                } else {
                    return true;
                }
            },

            // 选择banner图片
            selectImage1: function (e) {
                const file = e.target.files[0];
                if (file) {
                    this.editBannerImage = window.URL.createObjectURL(file)
                } else {
                    this.$refs.clearImageFile1.value = '';
                    this.editBannerImage = ''
                }
            },

            // 删除banner
            deleteBanner: function (e) {
                var self = this;

                this.$confirm('是否删除？', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    self.common.requestDataFile('/vk/updatebanners', 'POST', {
                        id: e.id,
                        status: 0
                    }).then((response) => {
                        self.$message.success('删除成功');
                        // 获取banner列表
                        self.getBannerList();
                    }).catch((error) => {
                        console.log(error);
                    })
                }).catch((error) => {
                    console.log(error);
                })
            },

            // 切换banner列表分页
            bannerCurrentChange: function (e) {
                this.bannerCurrentPage = e;
                // 获取banner列表
                this.getBannerList();
            },

            // 刷新
            refresh: function () {
                // 获取banner列表
                this.getBannerList();
            }
        }
    }
</script>

<style scoped>
    .banner-img {
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

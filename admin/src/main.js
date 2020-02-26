import '../theme/index.css'
import ElementUI from 'element-ui'
import Vue from 'vue'
import App from './App'
import router from './router'
import echarts from 'echarts'
import VueLazyLoad from 'vue-lazyload'
import axios from 'axios'
import VueAxios from 'vue-axios'

import global_ from '../static/config/global' // 自定义配置文件
import common from './util/common.js' // 引用公共js
import 'babel-polyfill'; // 让浏览器支持vuex Promise
require('echarts/theme/macarons');

Vue.use(ElementUI);
Vue.use(VueLazyLoad);
Vue.use(VueAxios, axios);
axios.defaults.baseURL = global_.BASE_URL;
axios.defaults.withCredentials = true;

Vue.config.productionTip = false;
Vue.prototype.GLOBAL = global_;
Vue.prototype.common = common;
Vue.prototype.$echarts = echarts;

const Bus = new Vue();

new Vue({
    el: '#app',
    render: h => h(App),
    router,
    components: {App},
    template: '<App/>',
    data() {
        return {
            Bus
        }
    }
});

import Vue from 'vue'
import Router from 'vue-router'

const login = () => import ('@/vue-pages/pages/login');
const index = () => import ('@/vue-pages/pages/index');
const user = () => import ('@/vue-pages/pages/user');
const information = () => import ('@/vue-pages/pages/information');
const banner = () => import ('@/vue-pages/pages/banner');

Vue.use(Router);

const router = new Router({
    mode: 'history',
    base: '/admin',
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) {
            return savedPosition
        } else if (to.hash) {
            return {
                selector: to.hash
            }
        } else {
            return {x: 0, y: 0}
        }
    },
    routes: [
        {
            path: '*',
            redirect: '/admin', // 默认路由
            component: login
        },
        {
            path: '/login', // 登陆
            name: 'login',
            component: login
        },
        {
            path: '/admin', // 入口页面
            component: index,
            children: [{
                path: '/', // 用户列表
                name: 'user',
                component: user
            }, {
                path: '/information', // 资讯列表
                name: 'information',
                component: information
            }, {
                path: '/banner', // 图片列表
                name: 'banner',
                component: banner
            }]
        }
    ]
});

router.beforeEach((to, from, next) => {
    // 这里填的是name
    let nextRoute = [
        'user', 'information', 'banner'
    ];
    let auth = localStorage.islogin;
    if (nextRoute.indexOf(to.name) > -1) {
        // 需要登录的路由
        if (auth) {
            // 已登陆
            next();
        } else {
            // 未登陆
            next({path: '/login', query: {redirect: Math.random()}});
        }
    } else {
        // 如果不需要登录
        if (auth && (to.name === 'login')) {  // 避免登录后再去登录页
            next({path: '/home'});
        }
    }
    next();

    // 路由发生变化修改页面title
    if (to.meta.title) {
        document.title = to.meta.title
    }
    next();
});

export default router;

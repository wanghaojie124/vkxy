webpackJsonp([6],{NHnr:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});n("Xcu2");var a=n("zL8q"),o=n.n(a),r=n("7+uW"),u={name:"App",data:function(){return{}},mounted:function(){this.landingOverdue()},methods:{landingOverdue:function(){if(localStorage.getItem("timeStamp")){var e=parseInt(localStorage.getItem("timeStamp"));(new Date).getTime()-e>432e5&&(localStorage.removeItem("timeStamp"),localStorage.removeItem("islogin"),this.$message({message:"登陆过期",type:"error"}))}}}},i={render:function(){var e=this.$createElement,t=this._self._c||e;return t("div",{attrs:{id:"app"}},[t("router-view")],1)},staticRenderFns:[]};var l=n("VU/8")(u,i,!1,function(e){n("WUfN")},null,null).exports,c=n("/ocq"),m=function(){return n.e(1).then(n.bind(null,"hmDJ"))};r.default.use(c.a);var p=new c.a({mode:"history",base:"/admin",scrollBehavior:function(e,t,n){return n||(e.hash?{selector:e.hash}:{x:0,y:0})},routes:[{path:"*",redirect:"/admin",component:m},{path:"/login",name:"login",component:m},{path:"/admin",component:function(){return n.e(0).then(n.bind(null,"wgCB"))},children:[{path:"/",name:"user",component:function(){return n.e(4).then(n.bind(null,"gfUV"))}},{path:"/information",name:"information",component:function(){return n.e(2).then(n.bind(null,"dgC9"))}},{path:"/banner",name:"banner",component:function(){return n.e(3).then(n.bind(null,"eT3b"))}}]}]});p.beforeEach(function(e,t,n){var a=localStorage.islogin;["user","information","banner"].indexOf(e.name)>-1?a?n():n({path:"/login",query:{redirect:Math.random()}}):a&&"login"===e.name&&n({path:"/home"}),n(),e.meta.title&&(document.title=e.meta.title),n()});var f=p,d=n("XLwt"),s=n.n(d),h=n("AXdl"),g=n("mtWM"),v=n.n(g),b=n("Rf8U"),w=n.n(b);var S={BASE_URL:"https://vkcampus.cdut.top"},y=n("//Fk"),A=n.n(y),L={requestData:function(e,t,n){return new A.a(function(a,o){v()({method:t,headers:{"Content-type":"application/json"},url:e,data:n}).then(function(e){a(e)}).catch(function(e){o(e)})})},requestDataParams:function(e,t,n){return new A.a(function(a,o){v()({method:t,headers:{"Content-type":"application/json"},url:e,params:n}).then(function(e){a(e)}).catch(function(e){o(e)})})},requestDataFile:function(e,t,n){var a=new FormData;for(var o in n)a.append(o,n[o]);return new A.a(function(n,o){v()({method:t,headers:{"Content-type":"multipart/form-data"},url:e,data:a}).then(function(e){n(e)}).catch(function(e){o(e)})})},loginOut:function(e){localStorage.removeItem("timeStamp"),localStorage.removeItem("islogin"),e.$router.push({path:"/login"})},collegeList:function(){return[{value:"西南交通大学",label:"西南交通大学"},{value:"四川师范大学",label:"四川师范大学"},{value:"四川大学",label:"四川大学"},{value:"电子科技大学",label:"电子科技大学"},{value:"成都理工大学",label:"成都理工大学"}]}};n("j1ja");n("tcAE"),r.default.use(o.a),r.default.use(h.a),r.default.use(w.a,v.a),v.a.defaults.baseURL=S.BASE_URL,v.a.defaults.withCredentials=!0,r.default.config.productionTip=!1,r.default.prototype.GLOBAL=S,r.default.prototype.common=L,r.default.prototype.$echarts=s.a;var U=new r.default;new r.default({el:"#app",render:function(e){return e(l)},router:f,components:{App:l},template:"<App/>",data:function(){return{Bus:U}}})},WUfN:function(e,t){},Xcu2:function(e,t){}},["NHnr"]);
//# sourceMappingURL=app.8fb5a5d9f14b5a88d44f.js.map
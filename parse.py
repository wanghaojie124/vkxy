"""
业务分析：
    1.抓取教务网信息存入数据库
    2.搭建api提供接口供小程序访问

spider: 编写爬虫文件，抓取数据并写入数据库
models: 提供可复用型代码
static: 一些静态文件
web: 路由

爬虫：
    1.课程，绩点，成绩
    2.验证码暂不进行跳过

数据库：
    用户：id，大学，专业，年级，绩点，
    学校：爬虫相关链接


API：
    小程序接口：
    返回json格式，


后台管理系统：
    功能：
    1.管理员可进行文章链接（跳转公众号文章链接）、图片上传，可查用户信息

时间安排：
    10.26日之前完善爬虫及数据库数据表的完整构建，以及部分路由
    10.30日之前完成后端路由及后台管理系统
    之后进行小程序接口调试。
"""

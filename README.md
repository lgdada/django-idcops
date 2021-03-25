# 简介

idcops 是一个基于Django开发，倾向于数据中心运营商使用的，拥有数据中心、客户、机柜、设备、跳线、物品、测试、文档等一系列模块的资源管理平台，解决各类资源集中管理与数据可视化的问题。
idcops 通过“数据中心”来分类管理每个数据中心下面的资源，每个数据中心均是单独的。

软件许可协议

django-idcops 遵循 Apache License 2.0。

## 联系

[作者博客](https://www.iloxp.com)

QQ群：185964462
[数据中心运维管理idcops](https://jq.qq.com/?_wv=1027&k=5SVIbPP)


### 捐赠该项目

![weixin](https://gitee.com/wenvki/django-idcops/raw/master/screenshots/wx_qr.jpg)
![zhifuba](https://gitee.com/wenvki/django-idcops/raw/master/screenshots/zfb_qr.jpg)


#### 项目截图：

[演示地址](http://idcops.iloxp.com/)

关注公众号回复体验获取 **体验** 账号

![weixin_qrcode](https://gitee.com/wenvki/django-idcops/raw/master/screenshots/qrcode_for_weixin.jpg)


![仪表盘](https://gitee.com/wenvki/django-idcops/raw/master/screenshots/2018-12-25_173535.jpg)


---

# 快速开始

#### 一、安装：

##### **1. 极速安装，支持WSL部署（推荐）**

需要联网，脚本一键自动安装

```
cd /opt
curl -sL https://gitee.com/wenvki/django-idcops/raw/master/auto_install.sh | sh

或
cd /opt
wget -q https://gitee.com/wenvki/django-idcops/raw/master/auto_install.sh
sh auto_install.sh

# 安装目录： /opt/django-idcops/ 
# 默认端口号： 18113 (gunicorn)，参数：SrvPort
# 默认idcops版本：develop，参数：VERSION develop[master]
# nginx 反向代理 18113 端口即可
```
[快速部署参考链接](https://mp.weixin.qq.com/s/fOcdTfr6274_Erh3fOftQw)


##### **2. docker-compose方式运行**

需要安装docker和docker-compose

```
WorkDir=/opt/
[ -d ${WorkDir} ]||mkdir -p ${WorkDir}
cd ${WorkDir}
# git clone https://github.com/Wenvki/django-idcops.git
git clone https://gitee.com/wenvki/django-idcops.git
cd ${WorkDir}/django-idcops
# 构建
docker-compose -f docker-compose.yml build --no-cache
# 启动
docker-compose -f docker-compose.yml up
# 新建超级管理员
# 按提示创建一个超级管理员admin用户和密码
docker-compose -f docker-compose.yml exec idcops python manage.py createsuperuser --username admin
# 停止运行
docker-compose -f docker-compose.yml stop
# 访问http://127.0.0.1:8000/
```

##### **3. 手动部署线上生产环境**

一步一步手动安装，可以进一步理解Django运行部署

[部署线上生产环境](https://www.iloxp.com/archive/2390/)


---

# 说明与项目截图

#### 二、初始化配置：

1、访问 http://your_ip:8000/
![login](https://gitee.com/wenvki/django-idcops/raw/master/screenshots/0001.png)


2、首次使用，系统还没有数据中心，需新建一个数据中心
![create idc](https://gitee.com/wenvki/django-idcops/raw/master/screenshots/0002.png)


3、自动重定向到首页 http://your_ip:8000/
![visit index](https://gitee.com/wenvki/django-idcops/raw/master/screenshots/0003.png)


---

#### 三、配置settings.py

`/opt/idcops_proj/idcops_proj/settings.py`


```
# django options
# 默认为： '/'
# 可配置为以 '/' 开始的字符串
# 例如： '/idcops/', 则 nginx 反向代理为： http://127.0.0.1:18113/idcops/
SITE_PREFIX = '/'

if SITE_PREFIX:
    SITE_PREFIX = SITE_PREFIX.rstrip('/') + '/'

STATIC_URL = '{}static/'.format(SITE_PREFIX)

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '{}media/'.format(SITE_PREFIX)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = '{}accounts/login/'.format(SITE_PREFIX)

LOGIN_REDIRECT_URL = '{}accounts/profile/'.format(SITE_PREFIX)

# idcops options

# SOFT_DELETE 设置为 `True`, 则执行删除的时候不会直接从数据库删除
SOFT_DELETE = True

# COLOR_TAGS 设置为 `True`, 相关标签会根据设置的颜色进行显示
COLOR_TAGS = True

# COLOR_FK_FIELD 设置为 `True`, 相关机房选项会根据设置的颜色进行显示
COLOR_FK_FIELD = False

```


#### 模块说明：

```
[
('syslog', 'log entries'), # 日志记录，核心内容，用于报表统计，日志分析等
('user', '用户信息'),
('idc', '数据中心'),  
('option', '机房选项'), # 机房选项，核心内容 ，系统元数据
('client', '客户信息'),
('rack', '机柜信息'),
('unit', 'U位信息'),
('pdu', 'PDU信息'),
('device', '设备信息'),
('online', '在线设备'),
('offline', '下线设备'),
('jumpline', '跳线信息'),
('testapply', '测试信息'),
('zonemap', '区域视图'),
('goods', '物品分类'),
('inventory', '库存物品'),
('document', '文档资料')
]
```


#### Thanks：

![JetBrains Community Support](https://gitee.com/wenvki/django-idcops/raw/master/screenshots/jetbrains.svg)

# django-idcops

django-idcops is a data center inventory management software.


# Quick start

1. Add `idcops` and `notifications` to your INSTALLED_APPS setting like this:
    ```
    INSTALLED_APPS = [
        ...
        'notifications',
        'idcops',
    ]
    ```

2. Include the idcops URLconf in your project urls.py like this:

    `path('idcops/', include('idcops.urls')),`

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/

5. Visit http://127.0.0.1:8000/idcops/ to participate in the build.

6. Project configuration options in settings.py:
```
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

AUTH_USER_MODEL = 'idcops.User'

# idcops settings

COLOR_BADGE = False

DELELE_SOFT = True
```

模块说明：
```
[
('syslog', 'log entries'), # 日志记录，核心内容，用于报表统计，日志分析等
('user', '用户信息'),  #用户信息
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

项目截图：

![仪表盘](https://raw.githubusercontent.com/Wenvki/django-idcops/master/screenshots/2018-12-25_173535.jpg)

![机房选项](https://raw.githubusercontent.com/Wenvki/django-idcops/master/screenshots/2018-12-25_173634.jpg)

![日志记录](https://raw.githubusercontent.com/Wenvki/django-idcops/master/screenshots/2018-12-25_173652.jpg)

![在线设备](https://raw.githubusercontent.com/Wenvki/django-idcops/master/screenshots/2018-12-25_173828.jpg)

![新建设备](https://raw.githubusercontent.com/Wenvki/django-idcops/master/screenshots/2018-12-25_173851.jpg)

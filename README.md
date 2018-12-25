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

6. settings extra setup example:
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

项目截图：

![仪表盘](https://raw.githubusercontent.com/Wenvki/django-idcops/master/screenshots/2018-12-25_173535.jpg)

![机房选项](https://raw.githubusercontent.com/Wenvki/django-idcops/master/screenshots/2018-12-25_173634.jpg)

![日志记录](https://raw.githubusercontent.com/Wenvki/django-idcops/master/screenshots/2018-12-25_173652.jpg)

![在线设备](https://raw.githubusercontent.com/Wenvki/django-idcops/master/screenshots/2018-12-25_173828.jpg)

![新建设备](https://raw.githubusercontent.com/Wenvki/django-idcops/master/screenshots/2018-12-25_173851.jpg)

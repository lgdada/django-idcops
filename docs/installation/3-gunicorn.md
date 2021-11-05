# Gunicorn

像大多数 Django 应用程序一样，idcops 作为 [WSGI 应用程序](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface) 在 HTTP 服务器后面运行。 本文档展示了如何为该角色安装和配置 [gunicorn](http://gunicorn.org/)（随 idcops 自动安装），但是其他 WSGI 服务器也可用并且应该也能正常工作。 [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) 是一种流行的替代方案。

## 配置

idcops 附带了 gunicorn 的默认配置文件。 要使用它，请将 `django-idcops/config/gunicorn.py`

```no-highlight
sudo cp /tmp/django-idcops/config/gunicorn.py /opt/django-idcops/config/gunicorn.py
```

虽然提供的配置应该足以满足大多数初始安装，但您可能希望编辑此文件以更改绑定的 IP 地址和/或端口号，或进行与性能相关的调整。 有关可用的配置参数，请参阅 [Gunicorn 文档](https://docs.gunicorn.org/en/stable/configure.html)。

## systemd 设置

我们将使用 systemd 来控制 gunicorn 和 idcops 的后台工作进程。 首先，将 `config/idcops.service` 复制到 `/etc/systemd/system/` 目录并重新加载 systemd 守护进程：

```no-highlight
sudo cp -v /opt/django-idcops/config/*.service /etc/systemd/system/
sudo systemctl daemon-reload
```

然后，启动 `idcops` 服务并使它们在启动时启动：

```no-highlight
sudo systemctl start idcops
sudo systemctl enable idcops
```

您可以使用命令 `systemctl status idcops` 来验证 WSGI 服务是否正在运行：

```no-highlight
systemctl status idcops.service
```

您应该会看到类似于以下内容的输出：

```no-highlight
● idcops.service - idcops WSGI Service
     Loaded: loaded (/etc/systemd/system/idcops.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2021-08-30 04:02:36 UTC; 14h ago
       Docs: https://django-idcops.readthedocs.io/en/stable/
   Main PID: 1140492 (gunicorn)
      Tasks: 19 (limit: 4683)
     Memory: 666.2M
     CGroup: /system.slice/idcops.service
             ├─1140492 /opt/django-idcops/env/bin/python3 /opt/django-idcops/env/bin/gunicorn --pid /va>
             ├─1140513 /opt/django-idcops/env/bin/python3 /opt/django-idcops/env/bin/gunicorn --pid /va>
             ├─1140514 /opt/django-idcops/env/bin/python3 /opt/django-idcops/env/bin/gunicorn --pid /va>
...
```

一旦您确认 WSGI 工作人员已启动并正在运行，请继续进行 HTTP 服务器设置。

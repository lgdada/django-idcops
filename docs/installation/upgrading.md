# 升级到新的 idcops 版本

## 查看发行说明

在升级您的 django-idcops 实例之前，请务必仔细查看自当前版本发布以来已发布的所有 [发行说明](../release/index.md)。 尽管升级过程通常不涉及额外的工作，但某些版本可能会引入破坏性或向后不兼容的更改。 这些在更改生效的版本下的发行说明中进行了说明。

## 将依赖项更新为所需版本

idcops 需要以下内容：

| Dependency | Minimum Version |
|------------|-----------------|
| Python     | 3.6             |

## 安装最新版本

与初始安装一样，您可以通过下载最新的发布包或克隆 git 存储库的“master”分支来升级 idcops。

### 选项 A：下载版本

从 GitHub 下载 [最新稳定版本](https://github.com/wenvki/django-idcops/releases) 作为 tarball 或 ZIP 存档。 将其解压缩到您想要的路径。 在这个例子中，我们将使用`/opt/django-idcops`。

下载并解压最新版本：

```no-highlight
wget https://github.com/wenvki/django-idcops/archive/vX.Y.Z.tar.gz
sudo tar -xzf vX.Y.Z.tar.gz -C /opt
sudo ln -sfn /opt/django-idcops-X.Y.Z/ /opt/django-idcops
```

将 `idcops/idcops_proj/settings.py`（如果存在）从当前安装复制到新版本：

```no-highlight
sudo cp /opt/django-idcops-X.Y.Z/idcops_proj/settings.py /opt/django-idcops/idcops_proj/settings.py
```

还要确保复制或链接您制作的任何自定义脚本和报告。 请注意，如果这些存储在项目根目录之外，则无需复制它们。 （如果不确定，请检查上面配置文件中的 `SCRIPTS_ROOT` 和 `REPORTS_ROOT` 参数。）

请务必复制您上传的媒体。 （所需的确切操作取决于您选择存储媒体的位置，但通常移动或复制媒体目录就足够了。）

```no-highlight
sudo cp -pr /opt/django-idcops-X.Y.Z/django-idcops/media/ /opt/django-idcops/django-idcops/
```

### 选项 B：克隆 Git 存储库

本指南假设 django-idcops 安装在 `/opt/django-idcops`。 下拉主分支的最新迭代：

```no-highlight
cd /opt/django-idcops
sudo git checkout master
sudo git pull origin master
```

## 运行升级脚本

一旦新代码就位，请验证您的部署所需的任何可选 Python 包（例如 `gunicorn` 或 `django`）是否在 `requirements.txt` 中列出。 然后，运行升级脚本：

```no-highlight
sudo ./upgrade.sh
```

此脚本执行以下操作：

<!-- * 销毁并重建 Python 虚拟环境 -->
* 安装所有需要的 Python 包（在 `requirements.txt` 中列出）
* 应用版本中包含的任何数据库迁移
* 收集所有由 HTTP 服务提供的静态文件
* 从数据库中删除陈旧的内容类型
* 从数据库中删除所有过期的用户会话

## 重启 django-idcops 服务

最后，重启 idcops gunicorn 服务：

```no-highlight
sudo sh /opt/django-idcops/scripts/stop.sh   #关闭服务
sudo sh /opt/django-idcops/scripts/start.sh  #启动服务
```

如果您要从不使用 Python 虚拟环境（v2.7.9 之前的任何版本）的安装进行升级，则需要在重新启动服务之前更新 systemd 服务文件以引用新的 Python 和 gunicorn 可执行文件。 它们位于`/opt/django-idcops/env/bin/`。

See the [housekeeping documentation](../administration/housekeeping.md) for further details.

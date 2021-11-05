# 安装 MySQL 数据库

本节涉及本地 MySQL 数据库的安装和配置。 如果您已经拥有 MySQL 数据库服务，请跳至 [下一节](2-idcops.md)。

!!! warning
    NetBox requires PostgreSQL 9.6 or higher. Please note that MySQL and other relational databases are **not** currently supported.

## 安装

=== "Ubuntu"

    ```no-highlight
    sudo apt update
    sudo apt install -y postgresql
    ```

=== "CentOS"

    ```no-highlight
    sudo yum install -y postgresql-server
    sudo postgresql-setup --initdb
    ```

    !!! info
        PostgreSQL 9.6 and later are available natively on CentOS 8.2. If using an earlier CentOS release, you may need to [install it from an RPM](https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/).

    CentOS configures ident host-based authentication for PostgreSQL by default. Because NetBox will need to authenticate using a username and password, modify `/var/lib/pgsql/data/pg_hba.conf` to support MD5 authentication by changing `ident` to `md5` for the lines below:

    ```no-highlight
    host    all             all             127.0.0.1/32            md5
    host    all             all             ::1/128                 md5
    ```

Once PostgreSQL has been installed, start the service and enable it to run at boot:

```no-highlight
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

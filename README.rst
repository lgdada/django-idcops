cd /home
git clone https://github.com/Wenvki/django-idcops.git mysite
cd mysite/
mkvirtualenv env # python虚拟环境
source env/bin/activate # 激活python虚拟环境
pip install -U pip # 升级pip
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser # 创建一个超级管理员用户
python manage.py runserver 0.0.0.0:8000 # 以django开发服务器运行软件

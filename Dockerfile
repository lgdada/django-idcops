FROM python:3.7-slim
ENV PYTHONUNBUFFERED 1

RUN mkdir /opt/django-idcops
WORKDIR /opt/django-idcops
COPY . /opt/django-idcops

RUN pip install --upgrade pip setuptools wheel -i https://mirrors.aliyun.com/pypi/simple/
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r /opt/django-idcops/requirements.txt || \
    pip install -r /opt/django-idcops/requirements.txt

COPY /opt/django-idcops/idcops_proj/settings_for_docker.py  /opt/django-idcops/idcops_proj/settings.py

VOLUME /opt/django-idcops/static
VOLUME /opt/django-idcops/media

#FROM ubuntu:20.04
#
#WORKDIR /app
#
#RUN apt-get update -y && \
#    apt-get install -y python3-pip python3-dev \
#    build-essential libssl-dev libffi-dev python3-setuptools \
#    python3-venv mongodb-clients bash-completion
#
## set environment variables
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#
#RUN python3.8 -m venv env
#RUN /bin/bash -c "source env/bin/activate"
#RUN pip install --upgrade pip
#COPY ./django/requirements.txt requirements.txt
#
##RUN pip3 install mysqlclient
#RUN pip3 install -r requirements.txt
##CMD [ "pip3", "install.py", "mysqlclient" ]
#
#COPY . .
##EXPOSE 8000
## CMD tail -f /dev/null
##CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]

# syntax = docker/dockerfile:1.2
# Dockerfile
# Django 최상위 루트에서 작성
FROM python:3.8
# 컨테이너 내에서 코드가 실행될 경로 설정
WORKDIR /app
# requirements.txt에 명시된 필요한 packages 설치
COPY ./django/requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Project를 /usr/src/app으로 복사
COPY . .
# 포트 설정
#EXPOSE 8000
# gunicorn 실행
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project_name.wsgi:application"]
# EXPOSE, CMD는 docker-compose에서 작성할 것이기 때문에, 동작하는지만 확인 후 주석or삭제 하도록 하자.
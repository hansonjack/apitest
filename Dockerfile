FROM python:3.7.7-alpine3.12

WORKDIR /usr/src/app
COPY ./requirements.txt .
COPY ./app.py .
COPY ./config.py .
COPY ./start.sh .
# 安装精简的mariadb依赖库
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && apk update \
    && apk --no-cache add tzdata nodejs npm build-base\
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && chmod +x start.sh \
    && npm install -g allure-commandline --save-dev

RUN ls -a
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --default-timeout=100
EXPOSE 5000
# CMD sh ./start.sh
CMD ["python","app.py"]
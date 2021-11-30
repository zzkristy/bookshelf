FROM python:3.6-buster

RUN echo '' > /etc/apt/sources.list \
    && echo 'deb http://mirrors.aliyun.com/debian/ buster main non-free contrib                ' >> /etc/apt/sources.list \
    && echo 'deb-src http://mirrors.aliyun.com/debian/ buster main non-free contrib            ' >> /etc/apt/sources.list \
    && echo 'deb http://mirrors.aliyun.com/debian-security buster/updates main                 ' >> /etc/apt/sources.list \
    && echo 'deb-src http://mirrors.aliyun.com/debian-security buster/updates main             ' >> /etc/apt/sources.list \
    # && echo 'deb http://mirrors.aliyun.com/debian/ buster-updates main non-free contrib        ' >> /etc/apt/sources.list \
    # && echo 'deb-src http://mirrors.aliyun.com/debian/ buster-updates main non-free contrib    ' >> /etc/apt/sources.list \
    && echo 'deb http://mirrors.aliyun.com/debian/ buster-backports main non-free contrib      ' >> /etc/apt/sources.list \
    && echo 'deb-src http://mirrors.aliyun.com/debian/ buster-backports main non-free contrib  ' >> /etc/apt/sources.list

RUN apt-get update \
    && apt-get install -y locales sudo vim \
    && localedef -i zh_CN -c -f UTF-8 -A /usr/share/locale/locale.alias zh_CN.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

# Set language and time zone
ENV LANG zh_CN.utf8
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Configure pip
ADD ./pip.conf /etc/pip.conf

# Install uwsgi
RUN pip3 install "uwsgi>=2.0.18,<3.0"
# Install uwsgitop
RUN pip3 install uwsgitop

WORKDIR  /opt/bookshelf

ADD ./requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

RUN mkdir -p logs

EXPOSE 8610

ENTRYPOINT  [ "run/entrypoint.sh" ]
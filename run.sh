#!/bin/bash

#开发、部署静态文件的脚本

root_path=$(cd `dirname $0`; pwd)

cd $root_path

#创建logs目录
if ! [[ -d logs ]];then
    mkdir logs
fi

if [ -z "$VIRTUAL_ENV" ];then
    python3 -m venv venv
    . venv/bin/activate
fi

pip3 install -r requirements.txt

export PYTHONPATH=$root_path/lib:$root_path:$PYTHONPATH
export DJANGO_SETTINGS_MODULE=bookshelf.settings

listen_port=8880

#if [[ x"$PYTHON" = "x" ]]; then
PYTHON=python3
#fi

command=$@
if ! [[ $# -gt 0 ]];then
    command="runserver 0.0.0.0:$listen_port --verbosity 3" #--noreload 可以关闭自动重启
elif [[ "$1" = "collectstatic" ]];then
    command="collectstatic --noinput -v0"
fi


$PYTHON $root_path/manage.py $command


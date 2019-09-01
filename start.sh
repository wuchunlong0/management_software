# -*- coding: utf-8 -*-
#!/usr/bin/env bash
pushd `dirname $0` > /dev/null
BASE_DIR=`pwd -P`
popd > /dev/null

#############
# Functions
#############
function logging {
    echo "[INFO] $*"
}

function build_venv {
    if [ ! -d env ]; then
        virtualenv env
    fi
    . env/bin/activate

    pip3 install -r requirements.txt
}


function del_db {
    logging "Clean"
    rm -rf "${BASE_DIR}/mysite/db.sqlite3"

    rm -rf "${BASE_DIR}/mysite/blog/migrations/0001_initial.py"
    ls "${BASE_DIR}/mysite/blog/migrations/"

    rm -rf "${BASE_DIR}/mysite/bank/migrations/0001_initial.py"
    ls "${BASE_DIR}/mysite/bank/migrations/"


    rm -rf "${BASE_DIR}/mysite/rbac/migrations/0001_initial.py"
    ls "${BASE_DIR}/mysite/rbac/migrations/"

    rm -rf "${BASE_DIR}/mysite/web/migrations/0001_initial.py"
    ls "${BASE_DIR}/mysite/web/migrations/"
}
function creator_db {
	logging "makemigrations" "blog"
	python "${BASE_DIR}/mysite/manage.py" "makemigrations" "blog"

    logging "makemigrations" "rbac"
    python "${BASE_DIR}/mysite/manage.py" "makemigrations" "rbac"

    logging "makemigrations" "web"
    python "${BASE_DIR}/mysite/manage.py" "makemigrations" "web"

    logging "makemigrations" "bank"
    python "${BASE_DIR}/mysite/manage.py" "makemigrations" "bank"

	
    logging "migrate"
	python "${BASE_DIR}/mysite/manage.py" "migrate"
}

function write_data_db {
	# logging "excel_import.py"
    # python "${BASE_DIR}/mysite/excel_import.py"
    logging "initdb.py"
	python "${BASE_DIR}/mysite/initdb.py"
    
}

function launch_webapp {
    cd ${BASE_DIR}/mysite
    python "manage.py" "runserver" "8000"
}

#############
# Main
#############
cd ${BASE_DIR}
OPT_ENV_FORCE=$1

build_venv

#放心操作!!! 创建数据库表，适合添加数据库后操作，能重复操作，不会破坏数据。
if [ "${OPT_ENV_FORCE}x" == "-cx" ];then    
    creator_db
fi
# 创建数据表、创建超级用户，不会破坏数据。一般情况不用操作，已经在write_data_db中实现此功能了。
if [ "${OPT_ENV_FORCE}x" == "-cax" ];then    
    creator_db
    python "${BASE_DIR}/manage.py" "createsuperuser" 
fi

# 初始化数据库。创建数据表,删除数据后再加载数据。谨慎操作！！！
if [ "${OPT_ENV_FORCE}x" == "-ix" ];then    
    del_db
    creator_db
    write_data_db
fi

#删除数据库表，数据不可恢复，谨慎操作！！！
if [ "${OPT_ENV_FORCE}x" == "-dx" ];then
	del_db
fi

launch_webapp

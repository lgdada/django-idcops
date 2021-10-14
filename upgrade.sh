#!/bin/sh

cd "$(dirname "$0")"
VIRTUALENV="$(pwd -P)/env"
PYTHON="${PYTHON:-python3}"

# 备份 `settings.py` 配置文件
if [ -f "idcops_proj/settings.py" ];then
    COMMAND="\cp -f idcops_proj/settings.py /tmp/"
    echo "backup \`settings.py\` configure file"
    eval $COMMAND
else
    echo "Warning: configure file \`idcops_proj/settings.py\` not exists"
fi

OLD_VER=$(git log --pretty=oneline|head -1|awk '{print $1}')
git fetch --all && git reset --hard origin/master && git pull
git diff --name-only ${OLD_VER}|grep 'requirements.txt'

if [ $? -eq 0 ];then
    
    which python3
    if [ $? -ne 0 ];then
        echo "Need install python3 version."
        exit 1
    fi
    
    # Remove the existing virtual environment (if any)
    if [ -d "$VIRTUALENV" ]; then
        COMMAND="\rm -rf ${VIRTUALENV}"
        echo "Removing old virtual environment..."
        eval $COMMAND
    else
        WARN_MISSING_VENV=1
    fi
    
    
    # Create a new virtual environment
    COMMAND="`which python3` -m venv ${VIRTUALENV}"
    echo "Creating a new virtual environment at ${VIRTUALENV}..."
    eval $COMMAND || {
        echo "--------------------------------------------------------------------"
        echo "ERROR: Failed to create the virtual environment. Check that you have"
        echo "the required system packages installed and the following path is"
        echo "writable: ${VIRTUALENV}"
        echo "--------------------------------------------------------------------"
        exit 1
    }
    # Activate the virtual environment
    . ${VIRTUALENV}/bin/activate
    
    # Install necessary system packages
    COMMAND="pip install wheel -i https://mirrors.aliyun.com/pypi/simple"
    echo "Installing Python system packages ($COMMAND)..."
    eval $COMMAND || exit 1
    
    # Install requirement packages
    COMMAND="pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple"
    echo "Installing Python requirement packages ($COMMAND)..."
    eval $COMMAND || exit 1
    
fi

. ${VIRTUALENV}/bin/activate

python manage.py makemigrations

# Test schema migrations integrity
COMMAND="python manage.py showmigrations"
eval $COMMAND > /dev/null 2>&1 || {
    echo "--------------------------------------------------------------------"
    echo "ERROR: Database schema migrations are out of synchronization. (No"
    echo "data has been lost.) . For further detail on the exact error,"
    echo "run the following commands:"
    echo ""
    echo "    source ${VIRTUALENV}/bin/activate"
    echo "    ${COMMAND}"
    echo "--------------------------------------------------------------------"
    exit 1
}

# 恢复 `settings.py` 配置文件
if [ -f "/tmp/settings.py" ];then
    COMMAND="\cp -f /tmp/settings.py idcops_proj/settings.py"
    echo "recovery \`settings.py\` configure file"
    eval $COMMAND
else
    echo "Warning: backup file \`/tmp/settings.py\` not exists"
fi

MIGRATE_TOTAL=$(python manage.py showmigrations|grep -E '\[ \]'|wc -l)
if [ ${MIGRATE_TOTAL} -gt 0 ];then
    python manage.py migrate
fi

# collect static files
python manage.py collectstatic --no-input

# Delete any expired user sessions
COMMAND="python manage.py clearsessions"
echo "Removing expired user sessions ($COMMAND)..."
eval $COMMAND || exit 1

echo "Upgrade complete! Don't forget to restart the idcops services:"
echo "  > /opt/django-idcops/scripts/stop.sh"
echo "  > /opt/django-idcops/scripts/start.sh"
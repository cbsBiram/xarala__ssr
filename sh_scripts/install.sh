#!/usr/bin/env bash
echo "***********************************************"
echo "***************** install *********************"
echo "***********************************************"

echo "***********************************************"
echo "---apt update e upgrade---"
echo "***********************************************"
apt-get -y update

echo "***********************************************"
echo "---OS dependencies---"
echo "***********************************************"
apt-get -y install python3-pip
apt-get -y install python3-dev python3-setuptools
apt-get -y install git
apt-get -y install supervisor
apt-get -y install virtualenv

# .....
# .....
# .....
# .....

echo "***********************************************"
echo "---install dependencies (including django)  ---"
echo "***********************************************"
pip3 install --upgrade pip
pip3 install --user pipenv
# activate env
# python3 -m venv xarala-env
# source xarala-env/bin/activate
# pip3 install -r requirements.txt
pipenv install
pipenv shell
python src/manage.py makemigrations
python src/manage.py migrate

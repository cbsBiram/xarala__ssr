#!/bin/sh

#   pip install -r requirements.txt
#  ./manage.py migrate
#   pipenv shell
ssh xarala@5.189.161.184 <<EOF
  cd pyapps/xarala_ssr
  git pull
  sudo systemctl restart ssr
  exit
EOF

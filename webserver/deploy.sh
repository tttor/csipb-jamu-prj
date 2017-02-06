#!/bin/bash
if [ "$#" -ne 8 ]; then
  echo "USAGE: bash deploy.sh -bak [0/1] -api [0/1] -predictor [0/1] -asset [0/1]"
  exit 1
fi

IJAH_SERVER=ijah@ijahserver
IJAH_DIR=/home/ijah/ijah/web
PREDICTOR_DIR=/home/ijah/ijah-predictor/python

if [ $2 -ne 0 ]; then
  echo "#######################################################################"
  echo "TODO: backing up ..."
  # stamp=`date +%Y-%m-%d-%H-%M-%S`
  # backdir='/home/ijah/ijah-backup/ijah-backup_'
  # cmd='mkdir '
  # cmd2=$cmd$backdir$stamp
  # ssh $IJAH_SERVER $cmd2
  # ssh $IJAH_SERVER find /var/www/ijah/ -type f ! -name "backup*" -exec cp --parents -t $backdir$stamp/ {} +
fi

#build the src in production stage
echo "#######################################################################"
echo 'Have you set the baseAPI to apps.cs at home.component.ts _and_ download.component.ts? [0/1]'
read baseAPISet
if [ "$baseAPISet" -ne 0 ]; then
  echo 'Yeay, lets roll...'
  echo "building then deploying dist ..."
  npm run build:prod
  scp -r dist/* $IJAH_SERVER:$IJAH_DIR
  scp -r src/app_home_graph_output.html $IJAH_SERVER:$IJAH_DIR
fi

if [ $4 -ne 0 ]; then
  echo "#######################################################################"
  echo 'Have you set the DB link to apps.cs at api/config.php? [0/1]'
  read dbLinkSet
  if [ "$dbLinkSet" -ne 0 ]; then
    echo "deploying APIs ..."
    scp -r api/* $IJAH_SERVER:$IJAH_DIR/api
  fi
fi

if [ $6 -ne 0 ]; then
  echo "#######################################################################"
  echo 'Have you set the DB link to apps.cs at predictor/config.py? [0/1]'
  read predictorConfigSet
  if [ "$predictorConfigSet" -ne 0 ]; then
    echo "deploying predictors ..."
    scp -r ../predictor/* $IJAH_SERVER:$PREDICTOR_DIR
  fi
fi

if [ $8 -ne 0 ]; then
  echo "#######################################################################"
  echo "deploying assets(css,img) ..."
  scp -r src/assets/css $IJAH_SERVER:$IJAH_DIR
  scp -r src/assets/img $IJAH_SERVER:$IJAH_DIR
fi

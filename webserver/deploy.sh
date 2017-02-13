#!/bin/bash
# $ npm install
# $ npm run start:hmr
# $ npm run build:prod
if [ "$#" -ne 6 ]; then
  echo "USAGE: bash deploy.sh -bak [0/1] -api [0/1] -predictor [0/1]"
  exit 1
fi

IJAH_SERVER=ijah@ijahserver
IJAH_DIR=/home/ijah/ijah/web
IJAH_DIR_STR='/home/ijah/ijah/web'
PREDICTOR_DIR=/home/ijah/ijah-predictor/python
BACKUP_DIR_STR='/home/ijah/ijah-backup/ijah-web-backup_'

if [ $2 -ne 0 ]; then
  echo "#######################################################################"
  echo "backing up ..."
  stamp=`date +%Y-%m-%d-%H-%M-%S`
  copyCMD='cp -r'
  cmd=$copyCMD' '$IJAH_DIR_STR' '$BACKUP_DIR_STR$stamp
  ssh $IJAH_SERVER $cmd

  rmCMD='rm -rf'
  arg1=$IJAH_DIR_STR'/main.*.bundle.js '
  arg2=$IJAH_DIR_STR'/polyfills.*.bundle.js '
  arg3=$IJAH_DIR_STR'/vendor.*.bundle.js '
  arg4=$IJAH_DIR_STR'/main.*.bundle.map '
  arg5=$IJAH_DIR_STR'/main.*.css '
  cmd2=$rmCMD' '$arg1$arg2$arg3$arg4$arg5
  ssh $IJAH_SERVER $cmd2
fi

#build the src in production stage
echo "#########################################################################"
echo 'Have you set the _version_ at app.component.html? [0/1]'
read vSet
echo 'Have you set the _baseAPI_ at home.component.ts _and_ download.component.ts? [0/1]'
read baseAPISet
if [ "$baseAPISet" -ne 0 ] && [ "$vSet" -ne 0 ]; then
  echo 'Yeay, lets roll...'
  echo "building then deploying dist ..."
  npm run build:prod
  scp -r dist/* $IJAH_SERVER:$IJAH_DIR
fi

if [ $4 -ne 0 ]; then
  echo "#######################################################################"
  echo 'Have you set the _DBlink_ at api/config.php? [0/1]'
  read dbLinkSet
  if [ "$dbLinkSet" -ne 0 ]; then
    echo "deploying APIs ..."
    scp -r api/* $IJAH_SERVER:$IJAH_DIR/api
  fi
fi

if [ $6 -ne 0 ]; then
  echo "#######################################################################"
  echo 'Have you set the _DBlink_ at predictor/config.py? [0/1]'
  read predictorConfigSet
  if [ "$predictorConfigSet" -ne 0 ]; then
    echo "deploying predictors ..."
    rm -f ../predictor/*.pyc
    scp -r ../predictor/* $IJAH_SERVER:$PREDICTOR_DIR
  fi
fi

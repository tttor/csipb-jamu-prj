#!/bin/bash
if [ "$#" -ne 12 ]; then
  echo "USAGE:"
  echo "bash deploy.sh -bak [0/1] -web [0/1] -api [0/1] -pred [0/1] -rsc [0/1] -dock [0/1]"
  exit 1
fi

SERVER=ijah@appcsserver
WEB_DIR=/home/ijah/ijah/web
WEB_DIR_STR='/home/ijah/ijah/web'
PREDICTOR_DIR=/home/ijah/ijah-predictor/python
BACKUP_DIR_STR='/home/ijah/ijah-backup/ijah-web-backup_'

# SERVER=ijah@agri.web.id
# WEB_DIR=/home/ijah/ijahweb
# WEB_DIR_STR='/home/ijah/ijahweb'
# PREDICTOR_DIR=/home/ijah/ijahpredictor
# BACKUP_DIR_STR='/home/ijah/ijah-backup/ijah-web-backup_'

# backup
if [ $2 -ne 0 ]; then
  echo "#######################################################################"
  echo "backing up _web_ only ..."
  stamp=`date +%Y-%m-%d-%H-%M-%S`
  copyCMD='cp -r'
  cmd=$copyCMD' '$WEB_DIR_STR' '$BACKUP_DIR_STR$stamp
  ssh $SERVER $cmd

  rmCMD='rm -rf'
  arg1=$WEB_DIR_STR'/main.*.bundle.js '
  arg2=$WEB_DIR_STR'/polyfills.*.bundle.js '
  arg3=$WEB_DIR_STR'/vendor.*.bundle.js '
  arg4=$WEB_DIR_STR'/main.*.bundle.map '
  arg5=$WEB_DIR_STR'/main.*.css '
  cmd2=$rmCMD' '$arg1$arg2$arg3$arg4$arg5
  ssh $SERVER $cmd2
fi

# web: build the src in production stage
if [ $4 -ne 0 ]; then
  echo "### WEB ###############################################################"
  echo 'Have you set the _version_ at app.component.html? [0/1]'
  read vSet
  echo 'Have you set the _baseAPI_ at home.component.ts _and_ download.component.ts? [0/1]'
  read baseAPISet
  if [ "$baseAPISet" -ne 0 ] && [ "$vSet" -ne 0 ]; then
    echo 'Yeay, lets roll...'
    echo "building then deploying dist ..."
    npm run build:prod
    scp -r dist/* $SERVER:$WEB_DIR
  fi
fi

# api
if [ $6 -ne 0 ]; then
  echo "#### API ##############################################################"
  echo 'Have you set the _DBlink_ at api/config.php? [0/1]'
  read dbLinkSet
  if [ "$dbLinkSet" -ne 0 ]; then
    echo "deploying APIs ..."
    scp -r api/* $SERVER:$WEB_DIR/api
    scp -r api_upload/* $SERVER:/home/ijah/node_api_docker/api_upload/
  fi
fi

# predictor
if [ $8 -ne 0 ]; then
  echo "#######################################################################"
  echo 'Have you set the _DBlink_ at config/credential.py? [0/1]'
  read predictorConfigSet
  if [ "$predictorConfigSet" -ne 0 ]; then
    echo "deploying predictors ..."

    find ../predictor/ -name "*.pyc" -type f -delete
    scp -r ../predictor/ $SERVER:$PREDICTOR_DIR

    find ../utility/ -name "*.pyc" -type f -delete
    scp -r ../utility/ $SERVER:$PREDICTOR_DIR

    find ../config/ -name "*.pyc" -type f -delete
    scp -r ../config/ $SERVER:$PREDICTOR_DIR
  fi
fi

# resource
if [ ${10} -ne 0 ]; then
  echo "### RSC ###############################################################"
  echo "deploying resource files ..."
  IJAH_MANUAL_ID=ijah_webserver_manual_id.pdf
  cp manual/manual-id/out/$IJAH_MANUAL_ID rsc/$IJAH_MANUAL_ID
  scp -r rsc/* $SERVER:$WEB_DIR/rsc
fi

# docker
if [ ${12} -ne 0 ]; then
  echo "### DOCKER ############################################################"
  echo "deploying docker files ..."
  scp ../docker/sh/start.sh ../docker/sh/stop.sh $SERVER:/home/ijah/
  scp ../docker/dockerfile/nodeapiDockerfile ../docker/sh/node_api_start_stop.sh ../docker/sh/node_api_build.sh $SERVER:/home/ijah/node_api_docker/
  # scp ../docker/dockerfile/webDockerfile $SERVER:/home/ijah/ijah/
  # scp ../docker/dockerfile/predictorDockerfile $SERVER:/home/ijah/ijah-predictor
fi

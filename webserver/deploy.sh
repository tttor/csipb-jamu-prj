#!/bin/bash
if [ "$#" -ne 6 ]; then
  echo "USAGE: bash deploy.sh -bak [0/1] -api [0/1] -asset [0/1]"
  exit 1
fi

if [ $2 -ne 0 ]; then
  echo "#######################################################################"
  echo "backing up /var/www/ijah at apps.cs..."
  stamp=`date +%Y-%m-%d-%H-%M-%S`
  backdir='/home/tor/ijah-backup/ijah-backup_'
  cmd='mkdir '
  cmd2=$cmd$backdir$stamp
  ssh tor@apps.cs.ipb.ac.id $cmd2
  ssh tor@apps.cs.ipb.ac.id find /var/www/ijah/ -type f ! -name "backup*" -exec cp --parents -t $backdir$stamp/ {} +
fi


#build the src in production stage
echo "#######################################################################"
echo 'Have you set the baseAPI to apps.cs at home.component.ts _and_ download.component.ts? [0/1]'
read baseAPISet
if [ "$baseAPISet" -ne 0 ]; then
  echo 'Yeay, lets roll...'
  echo "building then deploying dist ..."
  npm run build:prod
  scp -r dist/* tor@apps.cs.ipb.ac.id:/var/www/ijah/
  scp -r src/app_home_graph_output.html tor@apps.cs.ipb.ac.id:/var/www/ijah/
fi

if [ $4 -ne 0 ]; then
  echo "#######################################################################"
  echo 'Have you set the DB link to apps.cs at api/config.php? [0/1]'
  read dbLinkSet
  if [ "$dbLinkSet" -ne 0 ]; then
    echo "deploying APIs ..."
    scp -r api/* tor@apps.cs.ipb.ac.id:/var/www/ijah/api
  fi
fi

if [ $6 -ne 0 ]; then
  echo "#######################################################################"
  echo "deploying assets(css,img) ..."
  scp -r src/assets/css tor@apps.cs.ipb.ac.id:/var/www/ijah/
  scp -r src/assets/img tor@apps.cs.ipb.ac.id:/var/www/ijah/
fi

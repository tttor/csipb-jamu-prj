#!/bin/bash

#
echo 'Have you set the API to apps.cs at src/app/home/home.component.ts?'
read input

echo 'Have you set the DB link to apps.cs at api/config.php?'
read input2

echo 'Yeay, lets roll...'

#build the src in production stage
echo "building ..."
npm run build:prod

# backup existing content of ijah at apps.cs
echo "backing up ..."
stamp=`date +%Y-%m-%d-%H-%M-%S`
backdir='/home/tor/ijah-backup/ijah-backup_'
cmd='mkdir '
cmd2=$cmd$backdir$stamp

ssh tor@apps.cs.ipb.ac.id $cmd2
ssh tor@apps.cs.ipb.ac.id find /var/www/ijah/ -type f ! -name "backup*" -exec cp --parents -t $backdir$stamp/ {} +

# upload
echo "uploading files ..."
scp -r dist/* tor@apps.cs.ipb.ac.id:/var/www/ijah/
scp -r src/css tor@apps.cs.ipb.ac.id:/var/www/ijah/
scp -r src/img tor@apps.cs.ipb.ac.id:/var/www/ijah/
scp -r src/app_home_graph_output.html tor@apps.cs.ipb.ac.id:/var/www/ijah/
scp -r api/* tor@apps.cs.ipb.ac.id:/var/www/ijah/ijah

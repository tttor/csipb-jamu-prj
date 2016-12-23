#!/bin/bash

 #build the src in production stage
npm run build:prod

# backup existing content of ijah at apps.cs
stamp=`date +%Y-%m-%d-%H-%M-%S`
backdir='/var/www/ijah/backup_'
cmd='mkdir '
cmd2=$cmd$backdir$stamp

ssh tor@apps.cs.ipb.ac.id $cmd2

ssh tor@apps.cs.ipb.ac.id find ijah/ -type f ! -name "backup*" -exec cp --parents -t $backdir$stamp/ {} +
	
# #upload
scp -r dist/* tor@apps.cs.ipb.ac.id:/var/www/ijah/
scp -r src/css tor@apps.cs.ipb.ac.id:/var/www/ijah/
scp -r src/img tor@apps.cs.ipb.ac.id:/var/www/ijah/
scp -r src/output.html tor@apps.cs.ipb.ac.id:/var/www/ijah/
#scp -r /var/www/html/ijah

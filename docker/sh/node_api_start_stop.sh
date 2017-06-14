#!/bin/bash
if [ "$#" -ne 1 ]; then
  echo "USAGE:"
  echo "bash node_api_start_stop.sh [0/1]"
  exit 1
fi

if [ ${1} -eq 1 ]; then
  ################################################################################
  echo "Starting Ijah Node Uploader API.."
  docker run -d --restart=always \
         --name "ijah_node_API_daemon" \
         -p 2004:9001 \
         -v /home/ijah/ijah-uploads:/var/www/html/api_upload/uploads \
         ijah_node_api
fi

if [ ${1} -eq 0 ]; then
  echo "Stopping Ijah Node Uploader API..."
  docker stop ijah_node_API_daemon
  docker rm   ijah_node_API_daemon
fi
#!/bin/bash
if [ "$#" -ne 1 ]; then
  echo "USAGE:"
  echo "bash make_config.sh [dev/prod]"
  exit 1
fi
MODE=${1}

## database ########################################################################################
echo "making DATABASE config..."
cp "${MODE}_database_config.json" ../database/config_database.json

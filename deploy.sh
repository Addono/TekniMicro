#!/usr/bin/env bash

# Import environment variables from .env
export $(egrep -v '^#' .env | xargs)

echo "Generating config file"
python create_config.py || { echo "Failed generating configuration" ; exit 1; }

# Declare the list of files
declare -a files=(
    "config.json"
    "boot.py"
    "main.py"
    "config.py"
)

echo "Deploying to ${WEBREPL_HOST}"

# Copy all files
for i in "${files[@]}"
do
    source_path="src/${i}"
    target_path="/${i}"
    
    echo "Copying $source_path"

    webreplcmd put $source_path $target_path || { echo "Failed copying $source_path" ; exit 1 ; }
    #ampy put $source_path $target_path || { echo "Failed copying $source_path" ; exit 1 ; }
done

echo "All files copied"

echo "Restarting..."

# Using iwebrepl, because it actually terminates when the connection gets reset
iwebrepl --host $WEBREPL_HOST --password $WEBREPL_PASSWORD --port $WEBREPL_PORT --cmd 'import machine; machine.reset()' > /dev/null

echo "Done"

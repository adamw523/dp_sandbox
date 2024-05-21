#!/bin/sh

ENV_FILE_PATH=~/env/dp_sandbox.env

if [ -f "$ENV_FILE_PATH" ]; then
  while IFS= read -r line
  do
    # Ignore empty lines and lines starting with #
    if [ -n "$line" ] && [ "${line:0:1}" != "#" ]; then
      # Export the variable
      export "$line"
    fi
  done < "$ENV_FILE_PATH"
else
  echo "$ENV_FILE_PATH file not found."
fi
#!/bin/bash

aws lambda create-function \
--function-name $1 \
--zip-file fileb://${1}.zip \
--runtime python3.8 \
--role $2 \
--handler lambda_function.lambda_handler \
--timeout 60 \
--memory-size 256 \
--layers $3 \
--architectures x86_64 
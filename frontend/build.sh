#!/bin/bash

# get version from package.json
input_file="package.json"
data=`jq -r ".version" "$input_file"`
image="richli0623/word-replacer-admin"

# show version
echo "start building version $data ......."

docker buildx create --use

# build docker image
docker buildx build --platform linux/arm64 -t $image:latest -t $image:$data --push .

docker buildx rm
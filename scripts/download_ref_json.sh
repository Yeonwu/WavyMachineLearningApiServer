#!bin/bash

aws s3 cp s3://$REF_JSON_S3_BUCKET/$1 $REF_JSON_PATH/$1

if [ $? -eq 0 ]; then
	echo "success"
else
	echo "failed"
fi

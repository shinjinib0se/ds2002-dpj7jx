#!/bin/bash

# Assign arguments
LOCAL_FILE=$1
BUCKET_NAME=$2
EXPIRATION=${3:-604800} #default time of 7 days

# Upload the file to S3 (private by default)
aws s3 cp "$LOCAL_FILE" "s3://$BUCKET_NAME/"

# Generate a presigned URL
PRESIGNED_URL=$(aws s3 presign --expires-in "$EXPIRATION" "s3://$BUCKET_NAME/$(basename $LOCAL_FILE)")

echo "Presigned URL (expires in $EXPIRATION seconds):"
echo "$PRESIGNED_URL"

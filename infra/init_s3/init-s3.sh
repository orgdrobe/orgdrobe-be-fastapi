#!/bin/sh
set -e

ENDPOINT_URL="${AWS_ENDPOINT_URL:-http://seaweedfs-s3:8333}"
BUCKET_NAME="${S3_BUCKET_NAME:-media}"
CORS_CONFIG_PATH="${CORS_CONFIG_PATH:-/scripts/cors.json}"

echo "Waiting for SeaweedFS S3 gateway to become available at ${ENDPOINT_URL}..."
until aws --endpoint-url="$ENDPOINT_URL" s3 ls > /dev/null 2>&1; do
  echo "SeaweedFS S3 is not ready yet, retrying in 2s..."
  sleep 2
done

echo "SeaweedFS S3 gateway is online!"

# Create default bucket 'media' if it does not exist
if aws --endpoint-url="$ENDPOINT_URL" s3 ls "s3://${BUCKET_NAME}" > /dev/null 2>&1; then
  echo "Bucket '${BUCKET_NAME}' already exists."
else
  echo "Creating bucket '${BUCKET_NAME}'..."
  aws --endpoint-url="$ENDPOINT_URL" s3 mb "s3://${BUCKET_NAME}"
  echo "Bucket '${BUCKET_NAME}' created successfully."
fi

# Apply CORS configuration
if [ -f "$CORS_CONFIG_PATH" ]; then
  echo "Applying CORS policy to bucket '${BUCKET_NAME}' from ${CORS_CONFIG_PATH}..."
  aws --endpoint-url="$ENDPOINT_URL" s3api put-bucket-cors \
    --bucket "${BUCKET_NAME}" \
    --cors-configuration "file://${CORS_CONFIG_PATH}"
  echo "CORS policy applied successfully."
else
  echo "Notice: CORS configuration file not found at ${CORS_CONFIG_PATH}, skipping."
fi

echo "SeaweedFS S3 initialization finished successfully!"

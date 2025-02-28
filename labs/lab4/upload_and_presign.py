import boto3
import requests
import argparse
import os

def download_file(url, local_filename):
    #Download a file from a given URL and save it locally.
    print(f"Downloading file from {url}...")
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(local_filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded: {local_filename}")
    else:
        print("Error: Unable to download file.")
        exit(1)

def upload_to_s3(local_file, bucket_name):
    #Upload a file to an S3 bucket.
    s3 = boto3.client('s3', region_name="us-east-1")
    print(f"Uploading {local_file} to s3://{bucket_name}/ ...")
    try:
        s3.upload_file(local_file, bucket_name, local_file)
        print(f"File uploaded to s3://{bucket_name}/{local_file}")
    except Exception as e:
        print(f"Error uploading file: {e}")
        exit(1)

def generate_presigned_url(bucket_name, object_name, expires_in):
    #Generate a presigned URL for accessing the file in S3.
    s3 = boto3.client('s3', region_name="us-east-1")
    try:
        response = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_name},
            ExpiresIn=expires_in
        )
        return response
    except Exception as e:
        print(f"Error generating presigned URL: {e}")
        exit(1)

if __name__ == "__main__":
    # Setup command-line arguments using argparse
    parser = argparse.ArgumentParser(description="Download, upload to S3, and generate a presigned URL.")
    parser.add_argument("file_url", help="URL of the file to download.")
    parser.add_argument("bucket_name", help="Name of the S3 bucket.")
    parser.add_argument("--expiration", type=int, default=604800, help="Presigned URL expiration time in seconds (default: 7 days).")

    args = parser.parse_args()

    # Extract filename from the URL
    local_filename = os.path.basename(args.file_url)

    # Step 1: Download file
    download_file(args.file_url, local_filename)

    # Step 2: Upload file to S3
    upload_to_s3(local_filename, args.bucket_name)

    # Step 3: Generate presigned URL
    presigned_url = generate_presigned_url(args.bucket_name, local_filename, args.expiration)

    # Output presigned URL
    print(f"🔗 Presigned URL (expires in {args.expiration} seconds):\n{presigned_url}")

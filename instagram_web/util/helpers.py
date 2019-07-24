import boto3
import botocore
import os

S3_BUCKET = os.getenv('S3_BUCKET')
S3_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET = os.getenv('S3_SECRET_KEY')

s3 = boto3.client(
    "s3",
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)


def upload_file_to_s3(file, bucket_name, acl="public-read"):
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        print("Something happened: ", e)
        return e
    return file.filename

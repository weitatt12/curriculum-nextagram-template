import boto3
import botocore
import os

S3_BUCKET = os.getenv('S3_BUCKET')
S3_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET = os.getenv('S3_SECRET_KEY')



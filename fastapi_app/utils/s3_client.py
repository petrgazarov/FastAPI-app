import boto3
from fastapi_app import config

settings = config.get_settings()

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name="us-east-1",
)

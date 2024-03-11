import os

import aiobotocore
from aiobotocore.session import get_session

async def s3_upload(file_contents, bucket_name, key):
    # Configure S3 client using environment variables
    session = get_session()
    async with session.create_client(
            's3',
            endpoint_url=os.environ['S3_URL'],
            aws_access_key_id=os.environ['S3_ACCESS_KEY'],
            aws_secret_access_key=os.environ['S3_SECRET_KEY']
    ) as s3_client:
        # Upload the file to S3
        await s3_client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=file_contents
        )

    return True

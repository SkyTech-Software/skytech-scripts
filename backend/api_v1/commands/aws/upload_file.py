from backend.core.config import settings
import boto3
from io import BytesIO
from typing import Any


def upload_file_to_aws_storage(file_obj: bytes, object_name: str) -> Any:
    s3_client = boto3.client(
        "s3",
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )

    try:
        with BytesIO(file_obj) as file:
            s3_client.put_object(
                Bucket=settings.aws_access_point_alias, Key=object_name, Body=file
            )
            link_to_file = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": settings.aws_bucket_name, "Key": object_name},
                ExpiresIn=settings.aws_link_exp_time,
            )
            return link_to_file

    except Exception:
        pass

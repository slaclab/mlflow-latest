import boto3

aws_access_key_id = ""
aws_secret_access_key = ""
bucket_name = "mlflow-backup"
file_path = "wine-quality.csv"       # Local file to upload
object_name = "wine-quality.csv"    # How it will be named in S3

# If you have a custom S3 endpoint, pass endpoint_url="https://s3.yourprovider.com"
s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name="",   # optional if needed
    endpoint_url=""
)

# Upload the file
s3_client.upload_file(file_path, bucket_name, object_name)

print(f"Uploaded {file_path} to s3://{bucket_name}/{object_name}")


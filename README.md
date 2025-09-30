# MLFLOW

MLflow is an open-source platform to manage the complete ML lifecycle.

## Deployment
The [NCSA](https://github.com/ncsa/charts/tree/main/charts/mlflow) helm chart is used for this deployment.

```bash
helm upgrade  mlflow ncsa/mlflow --values values.yaml -n mlflow
```

Don't forget to update the image version in Dockerfile and Helm charts.

## Accessing S3 bucket

1. Create s3.ini
```bash
host_base = <url>
host_bucket = <url>
bucket_location = us-east-1
use_https = True

# Setup access keys
access_key = <key>
secret_key = <secret>

# Enable S3 v4 signature APIs
signature_v2 = false
``` 

2. Access the bucket with these commands 
```bash
s3cmd -c s3cmd.ini
s3cmd -c s3cmd.ini ls
s3cmd -c s3cmd.ini ls s3://mlflow
```

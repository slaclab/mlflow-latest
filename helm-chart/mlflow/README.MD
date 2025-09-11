# MLflow deployment in vlcuster
## Installation
Install krew - https://krew.sigs.k8s.io/docs/user-guide/setup/install/
Search for MinIO plugin -
```
kubectl krew search
kubectl krew install minio
kubectl krew info minio
 ~/.krew/bin/kubectl-minio init
kubectl minio tenant create mlflow-minio --interactive
kubectl create secret generic minio-credentials --from-literal=user=<username>--from-literal=key=<password> -n mlflow
```

Next, Create mlflow bucket in minio and reference the secret and minio hl url in values.yaml for s3. 

```
MLFlow:
  artifacts:
    bucketName: mlflow
.
.
.

s3:
  url: http://mlflow-minio-hl.mlflow.svc.cluster.local:9000
  # Secret with values for 'user' and 'key'
  secret: minio-credentials
```

Finally, install mlflow with custom values.yaml.
```
helm install mlflow ncsa/mlflow --values values.yaml -n mlflow
```
This is using [NCSA](https://github.com/ncsa/charts/tree/main) mlflow chart.
```
helm repo add ncsa https://opensource.ncsa.illinois.edu/charts/
helm repo add bitnami https://charts.bitnami.com/bitnami
helm dep update #to get the minio and postgresql charts referenced in the Chart.yaml
```

### Future Task
Get minio ingress running

# MLFLOW

MLflow is an open-source platform to manage the complete ML lifecycle. 

## Deployment
The [NCSA](https://github.com/ncsa/charts/tree/main/charts/mlflow) helm chart is used for this deployment. 

```bash
helm upgrade  mlflow ncsa/mlflow --values values.yaml -n mlflow
```

Don't forget to update the image version in Dockerfile and Helm charts.

#FROM python:3.8.13-slim
FROM --platform=linux/amd64 python:3.11-slim

# required by mysqclient
RUN apt-get update -y && \
    apt-get install -y python3-dev default-libmysqlclient-dev build-essential pkg-config

RUN pip install --upgrade pip
RUN pip install PyMySQL mysqlclient && \   
    pip install psycopg2-binary && \
    pip install mlflow[extras]==3.4.0 && \
    pip install boto3

ENV BACKEND_STORE_URI=
ENV DEFAULT_ARTIFACT_ROOT=/opt/artifact

EXPOSE 80

CMD ["sh", "-c", "mlflow server --host 0.0.0.0 --port 80 --gunicorn-opts \"$GUNICORN_OPTS\" --backend-store-uri $BACKEND_STORE_URI --artifacts-destination $ARTIFACTS_DESTINATION --serve-artifacts"]

import boto3
import pandas as pd
import yaml
import mlflow 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier 
from sklearn.metrics import accuracy_score 

with open("config.yaml") as f:
    config = yaml.safe_load(f)

aws_access_key_id = config["aws_access_key_id"]
aws_secret_access_key = config["aws_secret_access_key"]
bucket_name = config["bucket_name"]
object_name = config["object_name"]
local_file = "wine-quality.csv"
endpoint_url = config.get("endpoint_url")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name="us-east-1",   # optional if needed
    endpoint_url=endpoint_url
)

print(f"Downloading {object_name} from bucket {bucket_name}...")
s3_client.download_file(bucket_name, object_name, local_file)

df = pd.read_csv(local_file)
print("Dataset shape:", df.shape)
print(df.head())

X = df.drop("quality", axis=1)
y = df["quality"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

mlflow.set_tracking_uri("https://ard-mlflow.slac.stanford.edu")
mlflow.set_experiment("S3 Boto3 Demo")
mlflow.sklearn.autolog()

with mlflow.start_run() as run:
    model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    mlflow.log_metric("accuracy", acc)

    input_example = pd.DataFrame(X_train.iloc[:1])

    mlflow.sklearn.log_model(
        sk_model=model,
        name="model",
        registered_model_name="wine_quality_model",
        input_example=input_example
    )

    print("Run ID:", run.info.run_id)
    print("Accuracy logged:", acc)
    print("Model registered as: wine_quality_model")

model_uri = "models:/wine_quality_model/7"
loaded_model = mlflow.pyfunc.load_model(model_uri)
#model_uri = "mlartifacts/0/models/m-ce23c6a1b14b41a091e6c0b549122d0c/artifacts"
#model = mlflow.pyfunc.load_model(model_uri)
run_id = loaded_model.metadata.run_id
print(run_id)

sample = X_test.iloc[:5]
preds_loaded = loaded_model.predict(sample)
print("Sample predictions from registry:", preds_loaded)

df_compare = pd.DataFrame({
    "Actual": y_test.iloc[:5].values,
    "Predicted": preds_loaded}
        )
print("\nComparison of actual vs predictions:")
print(df_compare)


import os
import numpy as np
import mlflow
import boto3
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import warnings
warnings.filterwarnings('ignore')

# Set credentials and endpoint for MinIO directly in Python
os.environ['AWS_ACCESS_KEY_ID'] = 'minioadmin'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'minioadmin'
os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'http://localhost:9000'

# Create a boto3 session (optional, but can help debugging)
session = boto3.session.Session(
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    region_name='us-east-1'
)

# Dataset
X, y = make_classification(n_samples=1000, n_features=10, n_informative=2, n_redundant=8,
                           weights=[0.9, 0.1], flip_y=0, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)

# Model
params = {
    "solver": "lbfgs",
    "max_iter": 1000,
    "multi_class": "auto",
    "random_state": 8888,
}
lr = LogisticRegression(**params)
lr.fit(X_train, y_train)

y_pred = lr.predict(X_test)
report_dict = classification_report(y_test, y_pred, output_dict=True)
print(classification_report(y_test, y_pred))

# MLflow tracking
mlflow.set_tracking_uri("http://0.0.0.0:5000")
mlflow.set_experiment("First Experiment")

with mlflow.start_run():
    mlflow.log_params(params)
    mlflow.log_metrics({
        'accuracy': report_dict['accuracy'],
        'recall_class_0': report_dict['0']['recall'],
        'recall_class_1': report_dict['1']['recall'],
        'f1_score_macro': report_dict['macro avg']['f1-score']
    })
    mlflow.sklearn.log_model(lr, artifact_path="models")

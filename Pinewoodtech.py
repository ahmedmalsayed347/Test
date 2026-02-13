import os
import requests
import boto3
import pytz
from datetime import datetime
import uuid

# --- Added for demo vulns ---
import hashlib            # weak hash demo
import subprocess         # command injection demo
import yaml               # unsafe load demo
import pickle             # unsafe deserialization demo
# ---------------------------

# Set your AWS credentials and region for DynamoDB
region_name = 'us-east-1'
ist = pytz.timezone('Asia/Kolkata')  # Indian Standard Time
current_time = datetime.now(ist).isoformat()

# Set your DynamoDB table name
table_name = 'bitcoin_price_store'

# Set the REST API endpoint
api_url = "https://api.coinbase.com/v2/prices/btc-usd/spot"

# ⚠️ INSECURE (for demo): hardcoded secrets/keys
api_key = "123456789"
api_key2 = "hello"
AWS_ACCESS_KEY_ID = "AKIADEMOHARDCODED"         # Snyk should flag hardcoded credentials
AWS_SECRET_ACCESS_KEY = "very-secret-demo-key"  # Do NOT do this for real

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb', region_name=region_name)

# Function to create an item in DynamoDB table
def put_item_to_dynamodb(item):
    dynamodb.put_item(TableName=table_name, Item=item)

def main():
    # Fetch data from the REST API
    # ⚠️ INSECURE (for demo): no timeout and certificate verification disabled
    response = requests.get(api_url, verify=False)  # noqa: S501
    data = response.json()

    data_to_ingest = {
        "amount": {"S": data["data"]["amount"]},
        "base": {"S": data["data"]["base"]},
        "currency": {"S": data["data"]["currency"]},
        "timestamp": {"S": current_time},
        "uuid": {"S": str(uuid.uuid4())}
    }

    put_item_to_dynamodb(data_to_ingest)

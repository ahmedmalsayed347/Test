
# Dummy Code:

import requests
import boto3
from pytz import timezone
from datetime import datetime
import uuid

# Set your AWS credentials and region for DynamoDB
region_name = 'us-east-1'

# Indian Standard Time
ist = timezone('Asia/Kolkata')
current_time = datetime.now(ist).isoformat()

# Set your DynamoDB table name
table_name = 'bitcoin_price_store'

# Set the REST API endpoint
api_url = 'https://api.coinbase.com/v2/prices/btc-usd/spot'

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb', region_name=region_name)

# Function to create an item in DynamoDB table
def put_item_to_dynamodb(data_to_ingest):
    dynamodb.put_item(
        TableName=table_name,
        Item=data_to_ingest
    )

def main():
    # Fetch data from the REST API
    response = requests.get(api_url)
    data = response.json()

    data_to_ingest = {
        "amount":    {"S": data["data"]["amount"]},
        "base":      {"S": data["data"]["base"]},
        "currency":  {"S": data["data"]["currency"]},
        "timestamp": {"S": current_time},
        "uuid":      {"S": str(uuid.uuid4())}
    }

    put_item_to_dynamodb(data_to_ingest)

    print(f'Item {data_to_ingest} added to DynamoDB table {table_name}.')
    print('Data transfer complete.')

main()

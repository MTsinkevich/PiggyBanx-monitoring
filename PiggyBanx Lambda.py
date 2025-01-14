import boto3
import hashlib
import requests
import os

# Initialize AWS clients
s3 = boto3.client('s3')
sns = boto3.client('sns')

# Set your S3 bucket name and SNS topic ARN from environment variables
S3_BUCKET = os.environ['S3_BUCKET']
S3_KEY = 'last_website_hash.txt'
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']

# Website to monitor
URL = 'https://piggybanxinc.com/password'  # Replace with the URL you want to monitor

def get_website_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the website: {e}")
        return None

def hash_content(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def read_last_hash():
    try:
        s3.download_file(S3_BUCKET, S3_KEY, '/tmp/last_website_hash.txt')
        with open('/tmp/last_website_hash.txt', 'r') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error reading hash from S3: {e}")
        return None

def write_current_hash(current_hash):
    try:
        print(f"Writing hash: {current_hash}")
        with open('/tmp/last_website_hash.txt', 'w') as file:
            file.write(current_hash)
        print("Uploading hash file to S3...")
        s3.upload_file('/tmp/last_website_hash.txt', S3_BUCKET, S3_KEY)
        print("Hash file uploaded successfully.")
    except Exception as e:
        print(f"Error writing hash to S3: {e}")


def send_sns_notification(message):
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=message,
        Subject='Website Change Alert'
    )
    print(f"Notification sent: {message}")

def lambda_handler(event, context):
    content = get_website_content(URL)
    if not content:
        return {
            'statusCode': 500,
            'body': 'Failed to retrieve website content'
        }

    current_hash = hash_content(content)
    last_hash = read_last_hash()

    if last_hash != current_hash:
        print("Change detected!")
        send_sns_notification(f"Change detected on {URL}")
        write_current_hash(current_hash)
        return {
            'statusCode': 200,
            'body': 'Change detected and notification sent'
        }

    return {
        'statusCode': 200,
        'body': 'No changes detected'
    }

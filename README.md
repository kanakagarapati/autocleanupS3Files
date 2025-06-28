# autocleanupS3Files
# 🧹 Automated S3 Bucket Cleanup Using AWS Lambda and Boto3

## 📌 Objective

Automatically delete files older than 30 days from a specific Amazon S3 bucket using AWS Lambda and Boto3 (Python SDK).

---

## 🚀 Setup Instructions

### 1. ✅ Create S3 Bucket
- Go to **AWS Console → S3 → Create bucket**
- Example: `kanaka-s3-cleanup`
- Upload several files to the bucket (optional: simulate older files)
- **Note:** I have changed my system date and uploaded files in S3 bucket but AWS error out with below screen. So i have tried with DAYS_THRESHOLD: 0 days for now(On 28th June 2025) if my my Lambda function and IAM roles, S3 available Tomorrow that is on 29th June 2025 i will test with 1day older files.
- ![image](https://github.com/user-attachments/assets/5764f694-ec6d-4556-b9b6-2d2c3282b1d1)

- 

### 2. 🔐 Create IAM Role
- Go to **IAM → Roles → Create Role**
- Created IAM role with name `KanakaS3CleanupLambdaRole`
- Choose **Lambda** as trusted entity
- Attach policy: `AmazonS3FullAccess` (or custom policy below)
- Name it: `KanakaS3CleanupLambdaRole`
### 3. 🔐 Create Lambda function
- Go to **Lambda  → Create Function**
- Created lambda function with name `KanakaS3CleanupLambdaFunction`
```python
import boto3
from datetime import datetime, timezone, timedelta

# Initialize boto3 S3 client
s3 = boto3.client('s3')

# Change this to your bucket name
BUCKET_NAME = 'kanaka-s3-cleanup'
DAYS_THRESHOLD = 0

def lambda_handler(event, context):
    deleted_files = []
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=DAYS_THRESHOLD)
    
    try:
        # List all objects in the bucket
        response = s3.list_objects_v2(Bucket=BUCKET_NAME)
        
        if 'Contents' in response:
            for obj in response['Contents']:
                last_modified = obj['LastModified']
                if last_modified < cutoff_date:
                    s3.delete_object(Bucket=BUCKET_NAME, Key=obj['Key'])
                    deleted_files.append(obj['Key'])
        
        print(f"Deleted files: {deleted_files}" if deleted_files else "No files older than 30 days found.")
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

    return {
        'statusCode': 200,
        'body': f"Cleanup completed. Files deleted: {deleted_files}"
    }


```



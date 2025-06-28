import boto3
from datetime import datetime, timezone, timedelta

# Initialize boto3 S3 client
s3 = boto3.client('s3')

# Change this to your bucket name
BUCKET_NAME = 'kanaka-s3-cleanup'
DAYS_THRESHOLD = 30

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



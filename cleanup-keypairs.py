import boto3
import logging
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def delete_non_lab_key_pairs():
    try:
        # Initialize a session using environment variables or IAM roles
        ec2 = boto3.client('ec2', region_name=os.getenv('AWS_REGION', 'us-west-2'))
        
        # Describe key pairs
        key_pairs = ec2.describe_key_pairs()['KeyPairs']
        
        for key_pair in key_pairs:
            key_name = key_pair['KeyName']
            if 'lab' not in key_name:
                try:
                    ec2.delete_key_pair(KeyName=key_name)
                    logger.info(f"Deleted key pair: {key_name}")
                except ClientError as e:
                    logger.error(f"Failed to delete key pair {key_name}: {e}")
    except (NoCredentialsError, PartialCredentialsError) as e:
        logger.error(f"Credentials error: {e}")
    except ClientError as e:
        logger.error(f"Client error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    delete_non_lab_key_pairs()
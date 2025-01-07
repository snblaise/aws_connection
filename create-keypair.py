import boto3
import logging
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_key_pair(key_name):
    try:
        ec2 = boto3.client('ec2')
        key_pair = ec2.create_key_pair(KeyName=key_name)
        logger.info("Key pair created successfully")
        return key_pair['KeyMaterial']
    except NoCredentialsError:
        logger.error("Credentials not available")
    except PartialCredentialsError:
        logger.error("Incomplete credentials provided")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    key_name = os.getenv('AWS_KEY_NAME', 'SDK')
    key_material = create_key_pair(key_name)
    if key_material:
        # Save the key material to a file securely
        with open(f"{key_name}.pem", "w") as key_file:
            key_file.write(key_material)
        logger.info(f"Key material saved to {key_name}.pem")
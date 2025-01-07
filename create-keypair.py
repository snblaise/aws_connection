import boto3
import logging
import os
import stat
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

def save_key_material(key_name, key_material):
    try:
        file_path = f"{key_name}.pem"
        with open(file_path, "w") as key_file:
            os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)  # Set file permissions to read/write for the owner only
            key_file.write(key_material)
        logger.info(f"Key material saved to {file_path}")
    except IOError as e:
        logger.error(f"Failed to save key material: {e}")

if __name__ == "__main__":
    key_name = os.getenv('AWS_KEY_NAME', 'SDK')
    key_material = create_key_pair(key_name)
    if key_material:
        save_key_material(key_name, key_material)
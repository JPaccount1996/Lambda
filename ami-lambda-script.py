import boto3
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def lambda_handler(event, context):
    try:
        # AWS configurations
        instance_id = "i-0b899fd4a2057a10f"
        region = "us-east-1"

        # Create an EC2 client
        ec2_client = boto3.client('ec2', region_name=region)

        # Generate a unique name for the AMI
        ami_name = f"Backup-{instance_id}-{context.aws_request_id}"

        logger.info(f"Creating AMI for instance: {instance_id} with name: {ami_name}")

        # Create the AMI
        response = ec2_client.create_image(
            InstanceId=instance_id,
            Name=ami_name,
            Description="Backup AMI created by AWS Lambda",
            NoReboot=True
        )

        # Extract the AMI ID from the response
        ami_id = response['ImageId']

        logger.info(f"AMI creation initiated. AMI ID: {ami_id}")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "AMI creation initiated successfully",
                "ami_id": ami_id
            })
        }

    except Exception as e:
        logger.error(f"Error creating AMI: {str(e)}")

        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Error creating AMI",
                "error": str(e)
            })
        }

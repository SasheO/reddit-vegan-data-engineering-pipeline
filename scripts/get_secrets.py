"""
This hosts functions to get secrets from AWS secrets.
"""

import boto3
from botocore.exceptions import ClientError

def get_db_secrets(secret_name, region_name):
    """
    get_db_secrets gets the AWS Secrets for the database

    parameters:
        secret_name: (str) the name of the AWS secret 
        region_name: (str) the AWS region the secret is stored in
    
    returns: 
        secret: (str) the AWS secrets in a json-formattable string
    """

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString']
    return secret

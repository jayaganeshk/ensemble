import json
import boto3
import os

client = boto3.client('rds-data')

DB_NAME = os.environ.get('DB_NAME')
DB_ARN = os.environ.get('DB_ARN')
SECRETS_ARN = os.environ.get('SECRETS_ARN')


def execute_query(sql_statement):
    try:
        response = client.execute_statement(
            database="ensemble",
            resourceArn="arn:aws:rds:us-east-1:847397054438:cluster:ensemble-db",
            includeResultMetadata=True,
            secretArn="arn:aws:secretsmanager:us-east-1:847397054438:secret:ensemble-db-admin-password-wRZT4x",
            sql=sql_statement
        )
        return True
    except Exception as e:
        print(e)
        return e


def lambda_handler(event, context):
    # TODO implement
    print(event)

    body = json.loads(event['body'])
    print(body)
    # pneumonia_action
    result = "positive"
    sql_statement = "INSERT INTO pneumonia_action (user_id, pneumonia_action, result) VALUES ('" + \
        str(body['ID']) + "','" + body['URI'] + "','" + result + "')"

    print("sql_statement :", sql_statement)
    dbResponse = execute_query(sql_statement)
    print("dbResponse :", dbResponse)
    if(dbResponse):
        return {
            'statusCode': 200,
            'headers': {
                "content-Type": "application/json",
                "access-control-allow-origin": "*",
                "access-control-allow-methods": "GET,OPTIONS,DELETE, POST, PATCH",
                "access-control-allow-headers": "*"
            },
            'body': json.dumps(result)
        }
    else:
        return {
            'statusCode': 500,
            'headers': {
                "content-Type": "application/json",
                "access-control-allow-origin": "*",
                "access-control-allow-methods": "GET,OPTIONS,DELETE, POST, PATCH",
                "access-control-allow-headers": "*"
            },
            'body': json.dumps('There was some error')
        }

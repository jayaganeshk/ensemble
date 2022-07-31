import json
import boto3
import os

client = boto3.client('rds-data')

DB_NAME = "ensemble"
DB_ARN = "arn:aws:rds:us-east-1:847397054438:cluster:ensemble-db"
SECRETS_ARN = "arn:aws:secretsmanager:us-east-1:847397054438:secret:ensemble-db-admin-password-wRZT4x"


def execute_query(sql_statement):
    try:
        response = client.execute_statement(
            database=DB_NAME,
            resourceArn=DB_ARN,
            includeResultMetadata=True,
            secretArn=SECRETS_ARN,
            sql=sql_statement
        )
        if(response['ResponseMetadata']['HTTPStatusCode'] == 200):
            dbcols = []
            for col in response['columnMetadata']:
                dbcols.append(col['label'])
            result = []
            for record in response['records']:
                obj = {}
                for index, val in enumerate(record):
                    key = list(val.keys())[0]
                    obj[dbcols[index]] = val[key]
                result.append(obj)

            return result

    except Exception as e:
        print(e)
        return False


def generate_sql_statement(ID):
    statementQuery = "select * from pneumonia_action where user_id= " + str(ID)
    return statementQuery


def lambda_handler(event, context):
    print("event :", event)

    queryStringParameters = event['queryStringParameters']

    sql_statement = generate_sql_statement(queryStringParameters['id'])
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
            'body': json.dumps(dbResponse)
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

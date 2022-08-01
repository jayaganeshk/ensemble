import json
import boto3
import os

client = boto3.client('rds-data')
lambda_client = boto3.client('lambda')

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

def execute_select_query(sql_statement):
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


def generate_sql_statement(body):
    colsName = "("
    colsValue = "("
    for index, val in enumerate(body):
        if(len(body) - 1 == index):
            colsName += val
            colsValue += '"' + str(body[val]) + '"'
        else:
            colsName += val + ','
            colsValue += '"' + str(body[val]) + '", '
    colsName += ")"
    colsValue += ")"

    print("colsName :"+colsName)
    print("colsValue :"+colsValue)

    statementQuery = "INSERT INTO patient_details " + \
        colsName+" VALUES " + colsValue + " ;"

    return statementQuery


def predict_disease(symptoms):
    lambda_payload = {"Symptoms": symptoms}
    lambda_response = lambda_client.invoke(FunctionName='arn:aws:lambda:us-east-1:847397054438:function:abDiseasePrediction',
                                           InvocationType='RequestResponse',
                                           Payload=json.dumps(lambda_payload))
    precited = json.loads(
        lambda_response['Payload'].read().decode("UTF-8"))['body']
    print("precited :", precited)
    return precited


def lambda_handler(event, context):
    print("event :", event)
    body = json.loads(event['body'])
    print("event :", event)
    prediction = predict_disease(body["symptoms"])
    print("prediction: ", prediction)
    body['prognosis'] = prediction
    sql_statement = generate_sql_statement(body)
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
            'body': json.dumps(prediction)
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

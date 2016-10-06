#James Snee s3369721 Cloud Computing Assignment 2, 2016
from __future__ import print_function # Python 2/3 compatibility
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-west-2', endpoint_url="http://127.0.0.1:8000")

print('Creating table, please wait...')

table = dynamodb.create_table(
    TableName='Questions',
    KeySchema=[
        {
            'AttributeName': 'question',
            'KeyType': 'HASH'  #Partition key
        },
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'question',
            'AttributeType': 'S'
        },
		{
            'AttributeName': 'answer1',
            'AttributeType': 'S'
        },
		{
            'AttributeName': 'answer2',
            'AttributeType': 'S'
        },
		{
            'AttributeName': 'answer3',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'answer4',
            'AttributeType': 'S'
        },
		{
            'AttributeName': 'value1',
            'AttributeType': 'N'
        },
		{
            'AttributeName': 'value2',
            'AttributeType': 'N'
        },
		{
            'AttributeName': 'value3',
            'AttributeType': 'N'
        },
		{
            'AttributeName': 'value4',
            'AttributeType': 'N'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 10,
        'WriteCapacityUnits': 10
    }
)

print("Table status:", table.table_status)
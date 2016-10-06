from __future__ import print_function # Python 2/3 compatibility
import os
from boto import dynamodb2
from boto.dynamodb2.table import Table

TABLE_NAME = "cc-2016"
REGION = "us-west-2"

#open AWS Credentials file on hard drive and get Access Key ID and Secret Key
dir_path = os.environ['USERPROFILE'] + '\.aws\\'
f = open(dir_path + 'credentials', 'r')
lines = f.readlines()
first = lines[1].split('=')
second = lines[2].split('=')
AccessKey = first[1]
SecretKey = second[1]
#remove newline characters
AccessKey = AccessKey[:-1]
SecretKey = SecretKey[:-1]
print('Access Key: ' + AccessKey)
print('Secret Key: ' + SecretKey)
f.close()

print('Connecting to dynamodb...')

conn = dynamodb2.connect_to_region(
    REGION,
    aws_access_key_id=AccessKey,
    aws_secret_access_key=SecretKey,
)
table = Table(
    TABLE_NAME,
    connection=conn
)

print('Connected successfully!')

count = 0
#add data to table from CSV file
#CSV is delimited with | as we have commas in the questions
questionsfile = open('questions.csv', 'r')
for line in questionsfile:
    newLine = line.split('|')
    question_id = newLine[0]
    question = newLine[1]
    answer1 = newLine[2]
    answer2 = newLine[3]
    answer3 = newLine[4]
    answer4 = newLine[5]
    value1 = newLine[6]
    value2 = newLine[7]
    value3 = newLine[8]
    value4 = newLine[9]
    
    #create new item variable to add to database
    Item={
        'Id': count,
        'question_id': question_id,
        'question': question,
        'answer1': answer1,
        'answer2': answer2,
        'answer3': answer3,
        'answer4': answer4,
        'value1': value1,
        'value2': value2,
        'value3': value3,
        'value4': value4,
    }
    
    print('adding item to database...')
    table.put_item(data=Item)
    count = count + 1
    
print('Questions added to database.')
    
#cleanup
conn.close()    
    
    
    
    
    
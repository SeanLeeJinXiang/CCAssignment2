#James Snee s3369721 Cloud Computing Assignment 2, 2016
from __future__ import print_function # Python 2/3 compatibility
from flask import Flask, session, json, render_template, request
app = Flask(__name__)
import os
import json
import smtplib
from random import *
from boto import dynamodb2
from boto.dynamodb2.table import Table
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

#Global DynamoDB variables
TABLE_NAME = "cc-2016"
REGION = "us-west-2"
conn = None
table = None

#TODO: set high scores with name and score
#Possibly add Facebook API integration


#set a secret key for session variables
app.secret_key = 'o9/kTe4jN00s\'EsQQv425,3.'

#function to initialise counter and percentage
def initialiseVars():
        session['counter'] = 0
        session['percent'] = 0
        session['score'] = 0
        session['answer1'] = 10
        session['answer2'] = 5
        session['answer3'] = -5
        session['answer4'] = 0

#function to increment counter and percentage
def increment():
    try:
        session['counter'] += 1
        session['percent'] += 5
    except KeyError:
        session['counter'] = 1
        session['percent'] = 5


#index.html is inside templates folder
@app.route("/")
def main():
    create_connection()
    initialiseVars()
    return render_template('index.html')
    
@app.route('/showQuestion1')
@app.route('/showQuestion1/<question>')
def showQuestion1(question=None,answer1=None,answer2=None,answer3=None,answer4=None):
    #increment counter and percentage
    increment()
    print("Counter is at " + str(session['counter']))
    print("Percentage is at " + str(session['percent']))
    #generate random number between 0 and 14 to get that index from db
    random = randint(0, 14)
    print('Random number returned: ' + str(random))
    #get question from database
    response = getQuestion(random)
    #print response for testing only
    print('Response:')
    for i in response:
        #set question variable to pass to HTML from database
        question = i['question']
        answer1 = i['answer1']
        answer2 = i['answer2']
        answer3 = i['answer3']
        answer4 = i['answer4']
        
    return render_template('question1.html', question=question, answer1=answer1, answer2=answer2, answer3=answer3, answer4=answer4, counter=session['counter'], percent=session['percent'])

#button 1
@app.route('/pressButton1')
def pressButton1():
    print("You pressed button 1!")
    #increment score, percent and count
    session['counter'] += 1
    session['score'] += session['answer1']
    session['percent'] += 5
    print("score is now: " + str(session['score']))
    
    #generate random number between 0 and 14 to get that index from db
    random = randint(0, 14)
    print('Random number returned: ' + str(random))
    #get question from database
    response = getQuestion(random)
    #print response for testing only
    print('Response:')
    for i in response:
        #set question variable to pass to HTML from database
        question = i['question']
        answer1 = i['answer1']
        answer2 = i['answer2']
        answer3 = i['answer3']
        answer4 = i['answer4']
    
    
    if session['counter'] == 21:
            result = calculateScore()
            #save result into global
            session['result'] = result
            return render_template('results.html', score=session['score'], result_str=result)
    
    return render_template('question1.html', question=question, answer1=answer1, answer2=answer2, answer3=answer3, answer4=answer4, counter=session['counter'], percent=session['percent'])
    
#button 2
@app.route('/pressButton2')
def pressButton2():
    print("You pressed button 2!")
    #increment score, percent and count
    session['counter'] += 1
    session['score'] += session['answer2']
    session['percent'] += 5
    print("score is now: " + str(session['score']))
    
    #generate random number between 0 and 14 to get that index from db
    random = randint(0, 14)
    print('Random number returned: ' + str(random))
    #get question from database
    response = getQuestion(random)
    #print response for testing only
    print('Response:')
    for i in response:
        #set question variable to pass to HTML from database
        question = i['question']
        answer1 = i['answer1']
        answer2 = i['answer2']
        answer3 = i['answer3']
        answer4 = i['answer4']
    
    if session['counter'] == 21:
        result = calculateScore()
        #save result into global
        session['result'] = result
        return render_template('results.html', score=session['score'], result_str=result)
    
    return render_template('question1.html', question=question, answer1=answer1, answer2=answer2, answer3=answer3, answer4=answer4, counter=session['counter'], percent=session['percent'])
    
#button 3
@app.route('/pressButton3')
def pressButton3():
    print("You pressed button 3!")
    #increment score, percent and count
    session['counter'] += 1
    session['score'] += session['answer3']
    session['percent'] += 5
    print("score is now: " + str(session['score']))
    
    #generate random number between 0 and 14 to get that index from db
    random = randint(0, 14)
    print('Random number returned: ' + str(random))
    #get question from database
    response = getQuestion(random)
    #print response for testing only
    print('Response:')
    for i in response:
        #set question variable to pass to HTML from database
        question = i['question']
        answer1 = i['answer1']
        answer2 = i['answer2']
        answer3 = i['answer3']
        answer4 = i['answer4']
    
    if session['counter'] == 21:
        result = calculateScore()
        #save result into global
        session['result'] = result
        return render_template('results.html', score=session['score'], result_str=result)
    
    return render_template('question1.html', question=question, answer1=answer1, answer2=answer2, answer3=answer3, answer4=answer4, counter=session['counter'], percent=session['percent'])
    
#button 4
@app.route('/pressButton4')
def pressButton4():
    print("You pressed button 4!")
    #increment score, percent and count
    session['counter'] += 1
    session['score'] += session['answer4']
    session['percent'] += 5
    print("score is now: " + str(session['score']))
    
    #generate random number between 0 and 14 to get that index from db
    random = randint(0, 14)
    print('Random number returned: ' + str(random))
    #get question from database
    response = getQuestion(random)
    #print response for testing only
    print('Response:')
    for i in response:
        #set question variable to pass to HTML from database
        question = i['question']
        answer1 = i['answer1']
        answer2 = i['answer2']
        answer3 = i['answer3']
        answer4 = i['answer4']
    
    if session['counter'] == 21:
        result = calculateScore()
        #save result into global
        session['result'] = result
        return render_template('results.html', score=session['score'], result_str=result)
    
    return render_template('question1.html', question=question, answer1=answer1, answer2=answer2, answer3=answer3, answer4=answer4, counter=session['counter'], percent=session['percent'])
    
  
#Function to create connection to database
def create_connection():
    #This file will be stored on the server with the pages, will need to test
    #that this does not break
    #open credentials file to get AWS Access Key and Secret Key
    f = open('credentials', 'r')
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
    global table
    table = Table(
        TABLE_NAME,
        connection=conn
    )
    
    print('Connected successfully!')

    
#Function to get a question, it's answers and values from the DynamoDB    
def getQuestion(randomNum):
    #Query database with the Id of random number passed in
    try:
        #Boto3 lets you query any value in the database with <name>__eq (name equal)
        response = table.query(Id__eq = randomNum)
        print("Type of response: " + str(type(response)))

    except ClientError as e:
        print(e.response['Error']['Message'])
        
    return response

#function to calculate score
def calculateScore():
    ret_string = ""
    
    if session['score'] == 0:
        ret_string = "I am not sure how you are feeling. You answered \'Don't know\' to everything. Try the game again!"
    #if score goes below 0, put in the first category    
    elif session['score'] < 0:
        ret_string = "You are feeling pretty down in the dumps! It's ok though, help is always around you!"
    elif session['score'] >= 1 and session['score'] <= 49:
        ret_string = "You are feeling pretty down in the dumps! It's ok though, help is always around you!"
    elif session['score'] >= 50 and session['score'] <= 99:
        ret_string = "You aren't doing too well, poor thing! It's ok though, there are plenty of people around to help!"
    elif session['score'] >= 100 and session['score'] <= 149:
        ret_string = "You aren't overly happy, but you're also not overly sad, somewhere in the middle! Things could be better, but they also could be worse."
    elif session['score'] >= 150 and session['score'] <= 199:
        ret_string = "You are doing pretty well. There are some slight things bothering you, but it doesn't matter. Go you good thing!"
    elif session['score'] == 200:
        ret_string = "You are doing amazingly well! The sun is shining, the trees are green, absolutely nothing phases you!"
        
    return ret_string    

    
#load email form page
@app.route('/sendEmailForm')
def sendEmailForm():
    print('Email button pressed!')
    return render_template('sendEmail.html')
    

#function to send email
@app.route('/sendEmail', methods=['GET', 'POST'])
def sendEmail():
    
    #get value from the text field
    _email = request.form['email']
    
    #validate
    if _email:
        print("Email entered.")
    else:
        print("Email not entered!")
        
    #The following code will be using an @gmail.com account to send emails    
    
    FROM = 'moodquiz@gmail.com'
    TO = [_email]
    
    SUBJECT = "Your Mood Quiz Results!"

    TEXT = "Hi there! Your Mood Quiz Results are as follows: " + str(session['score']) + "\n" + str(session['result'])

    # Prepare actual message

    message = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    # Send the mail
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    #login with username and password
    server.login(FROM, "moodquiz1")
    server.sendmail(FROM, TO, message)
    server.quit()

        
    #when button is pushed, render homepage
    return render_template('emailsent.html')

    
if __name__ == "__main__":
    app.run(
        host='127.0.0.1',
        port=int("5000")
    )    
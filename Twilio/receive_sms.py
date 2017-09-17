from __future__ import print_function # In python 2.7
import sys
from twilio.twiml.messaging_response import MessagingResponse, Message
from flask import Flask, request, redirect, session
from pprint import pprint
import requests
import requests.auth
import json
import psycopg2


app = Flask(__name__)

def connectToDB( query ):
	try:
		connect_str = "dbname='textdiy' user='textdiy' host='localhost' " + \
			  "password='textdiypass'"
		# use our connection values to establish a connection
		conn = psycopg2.connect(connect_str)
		conn.autocommit = True
		# create a psycopg2 cursor that can execute queries
		cursor = conn.cursor()	
		cursor.execute(str( query ))
		return cursor.fetchall() 
	except Exception as e:
		print("Uh oh, can't connect. Invalid dbname, user or password? I am " + query[:3])
		print(e)



@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
	resp = MessagingResponse()
	message = Message()
	# Get the message the user sent our Twilio number
	from_ = str(request.values.get('From', None))[1:]
 	body = str(request.values.get('Body', None))	
	if len(connectToDB("SELECT * FROM tb_entity WHERE phone ilike '" + from_  + "';")) == 0:
		connectToDB("INSERT INTO tb_entity VALUES( default, '" + from_ + "');")
		message.body("Hey, we've never seen you here before! Welcome, we added you to the DB")
	else:
		message.body("Hey, we've seen you here before!")
	



	resp.append(message)
	return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

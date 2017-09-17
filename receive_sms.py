from __future__ import print_function # In python 2.7
import sys
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse, Message
from flask import Flask, request, redirect, session
from pprint import pprint
import requests
import requests.auth
import json
import psycopg2
import meetup.api


import googlemaps
from datetime import datetime

gmaps = googlemaps.Client(key='AIzaSyAR2OXiT53hrsAgwl4Cm9BCy-6Yiv_uTI0')

client = meetup.api.Client('14d567219591212802f2c32315851b')

city_meetup = 'Atlanta'

categ = client.GetFindGroups({'category': [15]}) #groups in "hobbies and crafts"



account_sid = "ACbe66967292816dd95aa89c4113e8a7d3"
auth_token = "20d83c1c9f1960831e026b8d351503fe"
client = Client(account_sid, auth_token)

thd_on_floor_help = [14046417973, 16314131686, 17064738144]

commands = "Heres a list of commands. Type in 'man <command>' to find out more about a specific command! \n\n* 'Man' \n\n* 'Commands' \n\n* 'DIY' \n\n* 'Filter' \n\n* 'Send Assistance To' \n\n* 'Closest' \n\n* 'Add Project' \n\n* 'Feedback' \n\n* 'Meetup'"
commands_dict = {}
commands_dict["diy"] = "'DIY' sends you five random projects. To pick a project to see the details of, please send back the name of the project. At any point in the conversation, feel free to text a keyword and you will receive 5 projects that contain the keyword."
commands_dict["filter"] = "'Filter <Popularity or Difficulty or Cost> < ,Beginner or Intermediate or Expert, Amount>' allows you to search up projects based on specific properties. Add a cost in dollars to the cost filter to see projects that cost less than that price to build (filter cost 50), and add a difficulty after 'filter difficulty' to get projects with either a beginner, intermediate, or expert level difficulty"
commands_dict["send assistance to"] = "'Send Assistance To' followed by the location you are at will send a text message to Home Depot workers working in your store. They will come and help you with your project!"
commands_dict["closest"] = "'Closest <zipcode>' gives you the Home Depot store closest to you!" 
commands_dict["add project"] = "'Add Project <Project URL>' lets us know you want a specific project to be added to the database. We will look over it and add it so that other people can also see it!"
commands_dict["feedback"] = "'Feedback <number of stars> <review>' leaves feedback for us so we can improve our product. We would love to hear what you guys think about it!" 
commands_dict["commands"] = "'Commands' will give you a list of commands you can run in this chatbot. The commands are not case-sensitive, but make sure you dont have anything before the command!"
commands_dict["meetup"] = "'Meetup' will find meetups with other DIY builders close by to you, and help you connect with the community!"






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

def newEntity( phone ):
	connectToDB("INSERT INTO tb_entity VALUES( default, '" + phone + "');")

@app.route("/website", methods=['GET', 'POST'])
def website_post():
	data = json.loads(request.data)
	phone = data['phone']
	print(phone)
	newEntity(phone)
	client.messages.create(
		to="+" + phone,
		from_="+12028398349",
		body="Hey, this is the DIY bot!",
	)
	return 'Recieved'



@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
	resp = MessagingResponse()
	message = Message()
	# Get the message the user sent our Twilio number
	from_ = str(request.values.get('From', None))[1:]
 	body = str(request.values.get('Body', None))	
	if len(connectToDB("SELECT * FROM tb_entity WHERE phone ilike '" + from_  + "';")) == 0:
		newEntity(from_)
		message.body("Hey, we've never seen you here before! Welcome to the DIY Chatbot!\n\n"  + commands) 
	else:
		if body.lower().strip() == "commands":
			message.body(commands)
		elif body.lower().strip() in ["hey", "hi", "hello", "welcome"]:
			message.body("Welcome to TextDIY Chatbot! Lets help you be a real DIY Builder :)\n\n" + commands)
		elif body.lower()[0:3] == "man":
			command_help = str(body.lower()[4:])	
			message.body(commands_dict[command_help])
		elif body.lower().strip() == "meetup":
			arr = []
			count = 0
			for x in categ.items:
				if count > 5:
					break
				else:
					if city_meetup in x.get('city') :
						arr.append(x.get('name') + "\n" + "Link: " + x.get('link'))
						count+=1
			text_message = "Here are meetups close by!\n"
			for x in arr:
				text_message += x + "\n\n"
			message.body(text_message)

		elif body.lower()[0:18] == "send assistance to":
			for number in thd_on_floor_help:
				client.messages.create(
					to="+" + str(number),
					from_="+12028398349",
					body="Hey, this is the DIY bot! Seems like someone needs help with a DIY project at" + body[15:] + ". You can call them at " + str(from_),
				) 
			message.body("Help is coming!")
		elif body.lower().strip() == 'diy':
			project_list = connectToDB("SELECT name FROM tb_project ORDER BY random() LIMIT 5;")
			body_string = ""
		 	for diy in project_list:
				body_string += str(diy[0]) + "\n\n"	
			message.body(body_string)
		
		elif body.lower()[0:7].lower() == "closest":
			location_array = body.lower().split()
			zipcode = location_array[1] 
			result = gmaps.places("Home Depot " + str(zipcode))
			address = result.get('results')[0].get('formatted_address')
			message.body(address)
	
		elif body.lower()[0:11] == "add project":
			diyrequest = body.lower().split()
			url_address = diyrequest[2]
			connectToDB("INSERT INTO tb_request VALUES(default, '" + str(url_address) + "');")
			message.body("Thanks for your addition! We recieved your request for a DIY project, we will review it and add it to out DIY database!")
		elif body.lower()[0:8] == "feedback":
			feedback = body.lower().split()
			stars = str(feedback[1])
			location_review = len(stars) + body.lower().find(stars)
			review = body.lower()[location_review:]
			connectToDB("INSERT INTO tb_feedback VALUES(default, " + stars  + ", '" + str(review) + "');")
			message.body("Thanks for your feeback! We will take it into account and imporve our product!")
			
	
		elif body.lower()[0:6] == 'filter':
			filter_array = body.lower().split()
			if filter_array[1] == 'popularity':
				popular = connectToDB("SELECT name, popularity FROM tb_project ORDER BY popularity DESC LIMIT 5")
				text = ""
				for item in popular:
					text += item[0] + ": Popularity of " + str(item[1]) + "\n\n"
				message.body(text)
			elif filter_array[1] == "cost":
				cost = connectToDB("SELECT name, cost FROM tb_project WHERE cost < " + str(filter_array[2]) + " ORDER BY cost DESC LIMIT 5")
				text = ""
				for item in cost:
					text += item[0] + ": Cost of " + str(item[1]) + "\n\n"
				message.body(text)
			elif filter_array[1] == "difficulty":
				difficulty = connectToDB("SELECT name, difficulty FROM tb_project WHERE difficulty ilike '" + str(filter_array[2]) + "' ORDER BY popularity LIMIT 5")
				text = ""
				for item in difficulty:
					text += item[0] + ": Difficulty of " + str(item[1]) + "\n\n"
				message.body(text)
		else:
			project_list = connectToDB("SELECT name FROM tb_project WHERE name ilike '%" + body + "%';")
			if len(project_list) == 0:
				message.body("There are no projects with that name. Please try again!")
			elif len(project_list) > 1:
				body_string = ""
				for diy in project_list:
					body_string += str(diy[0]) + "\n\n"	
				message.body(body_string)
			else:
				popularity = connectToDB("SELECT popularity FROM tb_project WHERE name ilike '%" + project_list[0][0] + "%'")[0][0]
				connectToDB("UPDATE tb_project SET popularity = " + str(popularity + 1) + " WHERE name ilike '%" + project_list[0][0] + "%';")
				link = connectToDB("SELECT address FROM tb_project WHERE name ilike '%" + project_list[0][0] + "%'")[0][0]		
				name = connectToDB("SELECT name FROM tb_project WHERE name ilike '%" + project_list[0][0] + "%'")[0][0]		
				tools = connectToDB("SELECT tools FROM tb_project WHERE name ilike '%" + project_list[0][0] + "%'")[0][0]		
				materials = connectToDB("SELECT materials FROM tb_project WHERE name ilike '%" + project_list[0][0] + "%'")[0][0]
				cost = connectToDB("SELECT cost FROM tb_project WHERE name ilike '%" + project_list[0][0] + "%'")[0][0]
				difficulty = connectToDB("SELECT difficulty FROM tb_project WHERE name ilike '%" + project_list[0][0] + "%'")[0][0]
				
				final_string =  link + "\n\n" + name + "\n" + "_________________" + "\n" + "Tools you'll need:" + "\n" +  tools + "\n\n" + "Materials:"+"\n" + materials + "\n\n" + "Cost: $" + str(cost) + "\n\n" + "Level: " + difficulty	
				message.body(final_string)

	resp.append(message)
	return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

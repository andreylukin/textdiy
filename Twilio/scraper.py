import gspread
from oauth2client.service_account import ServiceAccountCredentials
import psycopg2

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Woodworking Projects').sheet1

projects = sheet.get_all_values()

arr = []

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

for i in range(2, 39):
	vals = sheet.row_values(i)
	update = ""
	for j in range(len(vals)):
		newstr = vals[j].replace("[", "")
		newstr = newstr.replace("]", "")
		if (j == 5):
			update = update + newstr
		else:
			update = update + "'" + newstr + "'" + ", "

	arr.append(update)

for x in arr:
	connectToDB("INSERT INTO tb_project VALUES(default, " + x + ", 0);")

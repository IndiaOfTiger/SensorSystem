import sqlite3
import json
import pycurl
from io import BytesIO
import hashlib
import sys
import os
import time

######Default######
limit_default = "1000"
###################

def printTables(c):
	try:
		tables = c.execute("SELECT name FROM sqlite_master WHERE type='table';")
		print("Current Tables: %s" % str(tables.fetchall()))
	except:
		print("Error Executing Query")

def printQuery(query, c):
	try:
		printQuery = c.execute(query)
		queryList = []
		for row in printQuery:
			queryList.append(row)
			#print(row)
		return queryList
	except:
		print("Error Executing Query")

def curlToJson():	
	# Write data do dogData.json
	buffer = BytesIO()
	curl = pycurl.Curl()
	m = hashlib.sha1()
	
	#New
	host      = "https://api.dropap.com"
	
	#Old
	#host      = "https://s5-dropap.securepilot.com"
	
	uri       = "tracker/v1/get_device_record_by_key"
	api_key   = "BLAZING-nctu-daff6609x"
	secret    = "XXkpsmm19bn"
	mac       = "101a18000034,101a18000035"
	t_from    = "0000002000000";
	time      = "1484204053000";
	t_to      = "9484307000000";
	#t_from    = "1481592207000"
	#time      = "1481609423000"
	#t_to      = "1481609531000"
	index     = "0"
	limit     = limit_default
	m.update((secret+time).encode('utf-8'))
	api_token = m.hexdigest()
	
	curl.setopt(curl.URL,host + "/" + uri + "?api_key=" + api_key + "&api_token=" + api_token + "&time=" + time + "&mac=" + mac +
	 "&from=" + t_from + "&to=" + t_to + "&index=" + index + "&limit=" + limit)
	with open(os.path.join('.','dogData.json'), 'wb') as f:
		curl.setopt(curl.WRITEDATA, f)
		curl.perform()
	curl.close()

	#body = buffer.getvalue().decode('utf-8')
	#print(api_token)
	#print(body)

def connectAndStoreDB():
	databaseName = "dog.db"
	tableName = "dogData"
	tableAttrIni = """ReceiveTime TEXT PRIMARY KEY DESC, 
			Latitude TEXT, 
			Longitude TEXT, 
			DeviceName TEXT""";
	tableAttr = """ReceiveTime, 
			Latitude, 
			Longitude, 
			DeviceName""";
	db = sqlite3.connect(os.path.join('../../sqlite',databaseName))
	c = db.cursor()
	jsonFile = tableName + ".json"
	dogJson = json.load(open(os.path.join('.', jsonFile)))
	
	print("Connecting to %s" % databaseName)
	c.execute("DROP TABLE IF EXISTS dogData")
	printTables(c)
	
	c.execute("""CREATE TABLE IF NOT EXISTS %s(%s);""" % (tableName, tableAttrIni))
	#c.execute("SELECT name FROM sqlite_master WHERE type='table';")
	#print("Current Tables: " + str(c.fetchall()))
	printTables(c)
	
	columns = ['recv', 'GPS_N', 'GPS_E', 'device_name']
	for data_ in dogJson['value']['101a18000034']:
		keys = tuple(data_['data'][k] for k in columns)
		#print(str(keys))
		query = ("INSERT INTO %s (%s) VALUES %s;" % (tableName, tableAttr, (keys)))
		c.execute(query)
	for data_ in dogJson['value']['101a18000035']:
		keys = tuple(data_['data'][k] for k in columns)
		#print(str(keys))
		query = ("INSERT INTO %s (%s) VALUES %s;" % (tableName, tableAttr, (keys)))
		c.execute(query)

	db.commit()
	c.close()
	print("End Connection")
	#query = ("SELECT * FROM %s ;" % tableName)
	#printQuery(query)
def getLatLngOrder(Device, args):
	if args['number'] != None:
		limit_default = str(args['number'])
	databaseName = "dog.db"
	tableName = "dogData"
	db = sqlite3.connect(os.path.join('../../sqlite',databaseName))
	c = db.cursor()
	fff = args['From']
	ttt = args['To']
	print("Connecting to %s" % databaseName)
	curlToJson()
	connectAndStoreDB()
	print("%s:" % Device)
	if args['From'] != None :
		query = ("SELECT DISTINCT ReceiveTime,Latitude, Longitude, COUNT(*) FROM %s WHERE  (DeviceName = '%s' AND ReceiveTime < '%s' AND ReceiveTime > '%s') GROUP BY ReceiveTime" % (tableName,Device, ttt ,fff))
	else:
		query = ("SELECT DISTINCT ReceiveTime, Latitude, Longitude, COUNT(*) FROM %s WHERE DeviceName = '%s' GROUP BY Latitude, Longitude" % (tableName, Device))
	queryResult = printQuery(query,c)
	db.commit()
	c.close()
	print("End Connection")
	#print(queryResult)
	return queryResult


#connectAndStoreDB()
#getLatLngOrder('追蹤器_34')
#getLatLngOrder('Tracker_0035')



#!/usr/bin/env python3

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from googletrans import Translator
import datetime
import requests
import socket
import pickle
import sys

access_token = '157828~T0of10joslRvHUG30AuYFmlOPCPkpCtkMntAXH3jMfHXFU8GFFWHFNoDbVYnu3Lx'
api_url = 'https://virginia-tech-1.acme.instructure.com/api/v1/courses/96/files'

host = ''
port = 0
size = 0
back = 0

titles    = []
sentences = []
languages = ["en", "es", "fr", "zh-CN"]

translator = Translator()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def parameters():
	global host
	global port
	global size
	global back
	
	if(len(sys.argv) == 9):
		if(sys.argv[1] == "-h" and sys.argv[3] == "-p" and sys.argv[5] == "-s" and sys.argv[7] == "-b"):	
			host = sys.argv[2]
			port = int(sys.argv[4])
			size = int(sys.argv[6])
			back = int(sys.argv[8])
			
			print("System: saving server parameters.")
			
		else:
			print("Proper input params: -h <host> -p <port> -s <size> -b <backlog>")
			sys.exit("Error: invalid format of parameters.")
        
	else:
		print("Proper input params: -h <host> -p <port> -s <size> -b <backlog>")
		sys.exit("Error: invalid number of parameters.")

def setup():
	global server
	
	print("System: initializing server.")
	
	server.bind((host,port))
	server.listen(back)
	

def document():
	global title
	global sentences
	
	date = datetime.datetime.now()
	
	print("System: creating documents.")
		
	for language in languages:
		title = "lecture-" + language + "-" + str(date.day) + "-" + str(date.month) + "-" + str(date.year) + ".doc"
	
		titles.append(title)
	
		document = open(title, "w")
	
		for sentence in sentences:
			translation = translator.translate(sentence, dest = language)
		
			document.write(translation.text + "\n")
		
		document.close()
	
def upload():
	global titles
	
	session = requests.Session()
	session.headers = {'Authorization': 'Bearer %s' % access_token}
	
	print("System: uploading documents to Canvas.")
	
	for title in titles:
		payload = {}
		payload['name'] = title
		payload['parent_folder_path'] = '/'
		
		r = session.post(api_url, data = payload)
		r.raise_for_status()
		r = r.json()

		payload = list(r['upload_params'].items())

		with open(title, 'rb') as f:
			file_content = f.read()
			payload.append((u'file', file_content))
			r = requests.post(r['upload_url'], files = payload)
			r.raise_for_status() 
			r = r.json()
			
	print("System: uploading documents to Google Drive.")
	for title in titles: 
		gauth = GoogleAuth()
		gauth.LocalWebServerAuth()
		
		drive = GoogleDrive(gauth)
		
		file = drive.CreateFile()
		file.SetContentFile(title)
		file.Upload()
		print('title: %s, type: %s' % (file['title'], file['mimeType']))
		
	titles.clear()
		
	
	

def receive():
	global sentences
	global server
	
	while (1):
		client, address = server.accept()
	
		print("System: connecting to client.")
		
		data = pickle.loads(client.recv(size))
			
		print("System: recieved recorded sentences.")
			
		sentences = data
			
		document()
		upload()
				
		client.close()
	

def disconnect():
	print("System: exiting server program.")

def main():
	global sentences
	global server
	
	try:
		parameters()
		setup()
		receive()
			
	except KeyboardInterrupt:
		disconnect(client)

main()

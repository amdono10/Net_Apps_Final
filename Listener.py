#!/usr/bin/env python3

import speech_recognition as sr
import socket
import pickle
import sys

host = ''
port = 0
size = 0

sentences     = []
interjections = ["Oh", "Uh", "Well", "Hello", "Hey", "Hi", "However", "Regardless", "Nevertheless"]

client   = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
recorder = sr.Recognizer()

def parameters():
	global host
	global port
	global size
	
	if(len(sys.argv) == 7):
		if(sys.argv[1] == "-h" and sys.argv[3] == "-p" and sys.argv[5] == "-s"):	
			host = sys.argv[2]
			port = int(sys.argv[4])
			size = int(sys.argv[6])
			
			print("System: saving client parameters.")
			
		else:
			sys.exit("Error: invalid format of parameters.")
        
	else:
		sys.exit("Error: invalid number of parameters.")

		
def connect():
	global client
	
	try:
		client.connect((host,port))
		
		print("System: connecting to server.")
		
	except:
		sys.exit("Error: server connection refused.")
	
	
def record():
	global sentences
	
	print("System: beginning recording period.")
		
	with sr.Microphone() as source:
		while (1):		
			print("System: recording...")
			
			audio = recorder.listen(source)

			try:
				print("System: heard " + recorder.recognize_google(audio))

				if (recorder.recognize_google(audio) == "stop"):
					print("System: ending recording period.")
						
					break
						
				if (recorder.recognize_google(audio) == "redo"):
					print("System: rerecording previous sentence.")
						
					if (len(sentences) != 0):
							sentences.pop()
							
					else:
						print("Error: no sentences recorded.")
						
				else:
					sentences.append(recorder.recognize_google(audio))
					
					capitalize()
					punctuate()
						
			except sr.UnknownValueError:
				print("Error: Could not understand speech.")
					
			except sr.RequestError as error:
				print("Error: Could not request results from Google Speech Recognition service; {0}".format(error))
					
					
def capitalize():
	global sentences
	
	for it in range(len(sentences)):
		first = sentences[it][0].upper()

		sentences[it] = first + sentences[it][1:]


def punctuate():
	global sentences
	
	for it1 in range(len(sentences)):
		sentences[it1] = sentences[it1] + "."

		for it2 in range(len(interjections)):
			if(sentences[it1][0:len(interjections[it2])] == interjections[it2]):
				sentences[it1] = sentences[it1][0:len(interjections[it2])] + "," +  sentences[it1][len(interjections[it2]):]

def send():
	global sentences
	global client
	
	if(len(sentences) >= 1):
		print("System: sending recorded sentences.")
		
		client.send(pickle.dumps(sentences))
			
	else:
		print("System: no recorded sentences.")
		
		client.send(pickle.dumps("Message: empty."))

def disconnect():
	print("System: exiting recording program.")
		
	client.send(pickle.dumps("Message: exit"))
	client.close()

def main():
	try:
		parameters()
		connect()
		record()
		send()
		
	except KeyboardInterrupt:
		disconnect()
	
main()

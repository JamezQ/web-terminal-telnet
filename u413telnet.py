#!/usr/bin/python
import urllib2
import urllib
from BeautifulSoup import BeautifulSoup
import json
import html2text
import socket
HOST = ''
PORT = 9000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr

o = urllib2.build_opener( urllib2.HTTPCookieProcessor() )
urllib2.install_opener( o )

def Term():
	while True:
		try:
			conn.send("U413 > ")
			a = conn.recv(1024)[:-2]
			if a == "exit":
				break
			p = urllib.urlencode( { 'CommandString': a } )
			f = o.open( 'http://u413.com/Terminal/ExecuteCommand', p)
			
			data = f.read()
			f.close()
			
			data = json.loads(data)
			for i in range(4):
				data2 = data['DisplayArray'][i]['Text']
				data2 = data2.encode("ASCII",'replace')
				soup = BeautifulSoup(data2)
				
				Start.newhtml = html2text.html2text(str(soup))
				conn.send("\n")
				conn.send( Start.newhtml.replace("\n\n>","_"*76).replace("}\n\n","} ").encode("ASCII",'replace'))
		except:
			None
		if "logged out" in Start.newhtml:
			Start()
def Start():
	conn.send("Username: ")
	a = conn.recv(1024)[:-2]
	conn.send("Password: ")
	b = conn.recv(1024)[:-2]

	p = urllib.urlencode( { 'CommandString': 'login '+a+" "+b } )
	f = o.open( 'http://u413.com/Terminal/ExecuteCommand', p)

	data = f.read()
	f.close()

	data = json.loads(data)
	data = data['DisplayArray'][0]['Text']

	soup = BeautifulSoup(data)

	Start.newhtml = html2text.html2text(str(soup))
	conn.send( "\n")
	conn.send( Start.newhtml.encode("ASCII",'replace'))

	if "Invalid" in Start.newhtml:
		conn.send( "Try again\n")
		Start()
	else:
		Start.logged = True
		Term()

Start()



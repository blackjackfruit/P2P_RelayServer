#!/bin/python

import sys, time, socket
from select import select
from threading import Thread

# Connect two terminals to send UDP msgs to each other
# -p the port in which the host(which is you) allows for the client to connect to
# -c the client ip:port which you want to connect to
#python client.py -c 127.0.0.1:5001 -p 5001

class Receiver(Thread):
	continueReceiving = True
	def __init__(self,sock):
		Thread.__init__(self)
		self.sock = sock

	def senderObject(self, obj):
		self.senderObj = obj

	def run(self):
		while self.continueReceiving:
			ready = select([self.sock],[],[],1)
			if ready[0]:
				data, addr = self.sock.recvfrom(1024)
				if data == "end":
					self.senderObj.stop()
					break
				print "\nReceived: ", data
				sys.stdout.write(">")

	def stop(self):
		self.continueReceiving = False

class Sender(Thread):
	continueInput = True
	def __init__(self,ip,port,sock):
		Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.sock = sockd

	def receiverObject(self, obj):
		self.receiverObj = obj

	def run(self):
		sys.stdout.write(">")
		while self.continueInput:
			received = self.input_with_timeout(1,"")
			if received != "":
				self.sock.sendto(received, (self.ip, self.port))
				sys.stdout.write(">")

			if received == "end":
				self.receiverObj.stop()
				break

		print "Ended connection with client: " + self.ip + ":" + str(self.port)

	def stop(self):
		print "Exit Sender"
		self.continueInput = False

	def input_with_timeout(self,timeout,default):
	    sys.stdout.flush()
	    rlist, _, _ = select([sys.stdin], [], [], timeout)
	    if rlist:
	        s = sys.stdin.readline().replace('\n','')
	    else:
	        s = default
	    return s

args = sys.argv
argumentLen = len(sys.argv)

setup = ""

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

for num in range(1,argumentLen):
	
	if args[num] == "-c":
		c 			= args[num+1].split(':')
		client 		= c[0]
		clientPort	= int(c[1])

	if args[num] == "-p":
		port = int(args[num+1])

#TODO: error checking to make sure all variables are set

# make the socket to non-binding
s.setblocking(0)

# your ip address and port with which you want to enable the user to connect to
s.bind(("127.0.0.1",port))

sender = Sender(client,clientPort,s)
receiver = Receiver(s)

# both methods have a stop() function to stop the an infinite loop
# by passing the reference to the the other object, we can call the stop method when the word end is received
sender.receiverObject(receiver)
receiver.senderObject(sender)

# start threads duh
sender.start()
receiver.start()

# join threads to main thread
sender.join()
receiver.join()

# when both threads have finished executing, then close the connection
s.close()

print "Closed connection port: " + str(port)

import threading
import socket

#-----------
#FUNCTIONS
#-----------
def receive_messages(client):
	while not done:
		try:
			msg = (client.recv(1024).decode('utf-8'))
			if not done: 
				print("\n"+ msg + "\n>>", end='')
		except:
			print("Terminating receive thread")
			break

SERVER= "localhost"
PORT = 1234

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

done = False
while not done:

	# Make client receive messages on a separate thread
	receive_thread = threading.Thread(target=receive_messages, args=(server,))

	# Allows user to enter commands
	inputBuffer = input(">> ")
	if inputBuffer == "CONNECT":
		try: # Try connecting to the server when CONNECT is entered
			server.connect((SERVER, PORT))
			print("-Connection Established-")
			# Start receive thread once client has connected
			receive_thread.start()
		except: # Should the attempt fail, display an error so the program doesn't crash
			print("ERROR: Connection Failed.")

	# Tells server that the client wishes to quit the connection
	elif inputBuffer == "QUIT":
		server.send(inputBuffer.encode('utf-8'))
		done = True

	# Checks for SEND <message> with SEND and <message> separated by a space (' ')
	elif inputBuffer.split(' ')[0] == "SEND":
		server.send(inputBuffer[5:].encode('utf-8'))
	
	# If the wrong command is entered display an error message
	else:
		print("ERROR: Please use the CONNECT, SEND <message>, and QUIT commands.")
	
	
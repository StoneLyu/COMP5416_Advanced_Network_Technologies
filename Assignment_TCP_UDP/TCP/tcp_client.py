from socket import *
serverName = '192.168.111.130'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
sentence = raw_input('Input lowercase sentence:')
clientSocket.send(sentence)  # Do not specify serverName,serverPort
modifiedSentence = clientSocket.recv(1024)
print("From Server:", modifiedSentence)
clientSocket.close()

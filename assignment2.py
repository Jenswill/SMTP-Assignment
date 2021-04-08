import base64
from socket import *

#the message you want to send
msg = "\r\n Hello Jens! \r\n You have successfully sent an email, using your python script\r\n"

endmsg = ".\r\n"


subject = 'test' #the subject of the email

sender = 's205411@student.dtu.dk' #The sender of the mail
recvr = 's205411@student.dtu.dk' #The reciever of the mail

decodedFile = open("Python\DataCom\\assignment2\\assignment2.png","rb").read() #this opens the path to the image u want to attach the email
encodedFile = base64.b64encode(decodedFile) #And now it encodes the picture to base64

mailserver = ("localhost") 
clientSocket = socket(AF_INET, SOCK_STREAM) #creates the socket with two parametres. AF_INET refers to the ip-adress familiy IPV4
#                                           #and  SOCK_STREAM means that it is a TCP connection
clientSocket.connect((mailserver,2500)) # now the socket connects to the desired server, in this case it connects to 'localhost' with port: 2500


recv = clientSocket.recv(1024).decode() #Here the servers response is decoded

print(recv) # and the server response is printed
if recv[:3] != '220':
    print('220 reply not recieved from server.')

#Now we send the HELO command, to let the server know we want to use SMTP protocol
helocommand = 'HELO ' + mailserver + '\r\n' # EHLO for extended SMTP
clientSocket.send(helocommand.encode())

recv1 = clientSocket.recv(1024).decode() #The reply is decoded


if recv1[:3] != '250':
    print('250 reply not recieved from server.')
    
print(recv1)

#Now we specify who sends the email
mailfrom = 'MAIL FROM: ' + sender + '\r\n'
clientSocket.send(mailfrom.encode())

recv2 = clientSocket.recv(1024).decode()
if recv2[:3] != '250':
    print('250 reply not recieved from server.')
    
print(recv2)

#Now we specify who the reciever of the mail is
mailto = 'RCPT TO: ' + recvr + '\r\n'

clientSocket.send(mailto.encode())
recv3 = clientSocket.recv(1024).decode()

if recv3[:3] != '250':
    print('250 reply not recieved from server.')
print(recv3)

#Now we ask permission to send the mails data (The final data needs to be a \r\n.\r\n)
clientSocket.send(('DATA \r\n').encode())

recv4 = clientSocket.recv(1024).decode()
print(recv4)
if recv4[:3] != '354':
    print('354 reply not recieved from server.')


#Here the MIME connection is setup. The server therefore knows, that it should expect this format
clientSocket.send("MIME-Version: 1.0\r\n".encode())
#This specifies the content type of the MIME message we will send, and specifies the frontier that we use to change data-type
clientSocket.send('Content-Type: multipart/mixed; boundary=frontier\r\n'.encode())
#Now we save the frontier in a variable
frontier = '\r\n--frontier\r\n'.encode()

#Now we set the subject of the mail
sub = 'SUBJECT: ' + subject + '\r\n'

clientSocket.send(sub.encode())

#send what should be in the header 'FROM:'
mailfrom = 'FROM: ' + sender + '\r\n'
clientSocket.send(mailfrom.encode())

#send what should be in the header 'TO:'
mailto = 'TO: ' + recvr + '\r\n'

clientSocket.send(mailto.encode())


#We tell the server, that a new type of data is comming in
clientSocket.send(frontier)
#We tell the server, that the new content is plaing text;
clientSocket.send('Content-Type: text/plain\r\n'.encode())

#We send the message
clientSocket.send(msg.encode())
#We tell the server, that a new type of data is comming in
clientSocket.send(frontier)
#We tell the server, that the new content is an image of type PNG;
clientSocket.send('Content-Type: image/png\r\n'.encode())
#We tell the server, that it is being send in base64 encoding
clientSocket.send('Content-Transfer-Encoding: base64\r\n'.encode())
#We tell the server, that the upcomming file is an attatchment, and the filename is 'assignment2.png'
clientSocket.send("Content-Disposition: attachment; filename=assignment2.png\r\n".encode())
#Now we send the base64 encoded PNG
clientSocket.send('\r\n'.encode() + encodedFile + '\r\n'.encode())
#Now we tell the server, that our MIME message has finished (this is told by writing '--frontier--' instead of '--frontier')
clientSocket.send('--frontier--\r\n'.encode())
#At last we send the '.' on a line by itself, to let the server know that we are done with the DATA section
clientSocket.send(endmsg.encode())

#Now we recieve and print the servers reply;
recv6 = clientSocket.recv(1024).decode()
print(recv6)
if recv6[:3] != '250':
    print('250 reply not recieved from server.')
    
#And now we disconnect
clientSocket.send(('quit \r\n').encode() )

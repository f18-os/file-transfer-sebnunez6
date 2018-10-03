##File Server
Server will receive messages and run each client that connects in a file.  
When receiving messages from the client it will take the first message,
as the name of the child. Then proceed to receive the file until the
key word "end" is sent to the server. The server will then close the file 
and the child will terminate. Any file the Server receives will be
 located inside the Server Folder.

##File Client
Option is given whether the user wants to or doesn't want to use the stammer
proxy. The client will list the current files available then send them to the server.
The client will send a beginning message with the name of the file accompanied
by start to tell the server that it will now receive the file content. The client 
will then traverse the file 100 bytes at a time. Once the file has been fully
 traversed the client sends an end message to signify the end 
 of the file to the server

##Fairy Song
Test file

#Collab
Part of code received from Freudenthal

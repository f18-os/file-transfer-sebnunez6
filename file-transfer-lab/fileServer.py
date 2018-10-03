#! /usr/bin/env python3
import sys, re, socket, os 
sys.path.append("../lib")       # for params
import params
os.chdir("Server") #changes os to Server Directory for Files
switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
while True:
    print("listening on:", bindAddr)

    sock, addr = lsock.accept()
    
    #creates child to handle accepted connection
    rc = os.fork()
    if rc == 0:
        print("connection rec'd from", addr)

        from framedSock import framedSend, framedReceive

        start = framedReceive(sock, debug)
        try:
            start = start.decode()
        except AttributeError:
            print("error exiting: ", start)
            sys.exit(0)
        
        #gets rid of any characters not involved with the filename
        count = 0
        for char in start:
                    if char.isalpha():
                        break
                    else:
                        count = count + 1
        start = start[count:]

        #tells server where file name ends
        start = start.split("\'start\'")

        #opening file
        file = open(start[0].strip(),"wb+")

        #Receives input while file has not ended
        while True:
            #error handling
            try:
                payload = framedReceive(sock, debug)
              
            except:
                pass

            #checking for debugging
            if debug: print("rec'd: ", payload)
            if not payload:
                break
            #checking if end of file else writes to file
            if b"\'end\'" in payload:
                file.close()
                sys.exit(0)
            else:
                file.write(payload[1:])

        #ensures child exits while loop
        break
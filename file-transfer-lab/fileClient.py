#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os

sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "fileClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

files = os.listdir(os.curdir)  #grab current files
print(files)
inputFile = input("Please select a file to send \n")
#Attemps to read input as file
try:
    with open(inputFile.strip(),"rb") as binary_file:
        # Read the whole file at once
        data = binary_file.read()
except FileNotFoundError:
    print("file not found exiting")
    sys.exit(0)

#sends file information to server
framedSend(s,b':' +inputFile.strip().encode('utf-8') + b"\'start\'")

#Gets rid of new line character due to sending error by replacing it with 'e'
data = data.replace(b"\n", b"\'e\'")

#Sends 100 bits at a time to server
while len(data) >= 100:
    line = data[:100]
    data = data[100:]
    framedSend(s,b":"+line,debug)

#sends left over bits
if len(data) > 0:
    framedSend(s,b":"+data,debug)

#tells server file has ended
framedSend(s,b":\'end\'")



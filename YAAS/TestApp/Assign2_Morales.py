__author__ = 'Miguel Morales'

import datetime
import re
import time

def is_it_friday(d):
    if d.isoweekday()==5:
        return "Yes, it is Friday!"
    else:
        return "Nope."

import socket
PORT=8080
HOST="127.0.0.1"

def getHeader(connection):
    currentChunk = connection.recv(1)
    recievedMsg = currentChunk
    while currentChunk != '':
        currentChunk = connection.recv(1)
        recievedMsg = recievedMsg + currentChunk
        if "\r\n\r\n" in recievedMsg:
            break
    return recievedMsg

def getContentLenght(header):
    lines = header.split("\r\n")
    for line in lines:
        if "Content-Length:" in line:
            s = line.split(":")
            return int(s[1])
    return 0

def getBody(connection, contentLenght):
    return connection.recv(contentLenght)


def parse_request(request, connection):
    lines=request

    if len(lines)<1:
        return None
    words=lines.split()

    if len(words)<3:
        return None

    print "words: ", str(words)

    if words[0]=="GET" or words[0]=="POST" and words[2] in ["HTTP/1.0","HTTP/1.1"]:
        method = words[0]
        url = words[1]

        if words[0]=="POST":
            print "Someone did a POST!!"
            contentLenght = getContentLenght(request)
            post_data = ""
            if contentLenght!= 0:
                data_line = getBody(connection, contentLenght)
                print "This is the dataline!!"+data_line
                return (method, url, data_line)

        else:
            return (method, url, [])
    else:
        return None



def server(handler, port=PORT, host=HOST, queue_size=5):
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysocket.bind((host, port))
    mysocket.listen(queue_size)
    while True:
        print "Waiting at http://%s:%d" % (host, port)
        (connection, addr) = mysocket.accept()
        print "New connection", connection, addr
        handler(connection)
        connection.close()
        print "Connection closed."

def sendResponse(response, connection):
    connection.sendall(response)

def create_document(body):
    return "<html><body>\n\r"+body+"</body></html>\n\r"

def create_response(status,content,content_type="text/html"):
    return "HTTP/1.1 "+status+"\n\r"+ \
    "Content-Type: "+content_type+";\n\r\n\r"+ \
    content+"\n\r"

def create_form():
    return '<form method="POST" action="/formresult">\n\r'+ \
            '<div>Date: <input name="date" type="text"/> <br>\n\r'+\
            ' Password: <input name="password" type="password"/> <br> \n\r'+ \
           '<input type="submit"/></div> </form>'

def fridayWebapp(connection):

    header = getHeader(connection)
    parameters = parse_request(header, connection)

    if parameters[0]=="GET":
        if parameters[1]=="/":
            response=create_response(
                "200 OK",
                create_document(is_it_friday(datetime.date.today()))
                )
        elif parameters[1]=="/dateform":
            response=create_response(
                "200 OK",
                create_document(create_form())
                )
        elif re.match("/(\d{8})$",parameters[1]) is not None:
            print parameters[1]
            date = datetime.datetime.strptime(parameters[1], "/%d%m%Y")
            response=create_response(
                "200 OK",
                create_document(is_it_friday(date))
                )
        elif parameters[1]=="/log":
            f=open("log.txt")
            text=""
            for line in f:
                text += line+"<br>"

            response=create_response(
                "200 OK",
                create_document(text)
                )
        else:
            response=create_response(
               "400 Bad Request",
                create_document("Bad Request pal!")
                )
    elif parameters[0]=="POST" and parameters[1]=="/formresult":
        result=re.match("date=(?P<date>\d{8})&password=(?P<pass>.*)",parameters[2])
        if result is not None:
            s_date=result.group("date")
            print "date: "+s_date
            pwd=result.group("pass")
            if pwd=="123":
                date = datetime.datetime.strptime(s_date, "%d%m%Y")
                response=create_response(
                    "200 OK",
                    create_document(is_it_friday(date))
                    )
            else:
                f=open("log.txt","a")
                f.write(time.strftime("%d-%m-%Y %X") + " user entered incorrect password: "+pwd+"\n\r")
                f.close()
                response=create_response(
                   "400 Bad Request",
                    create_document("You entered a bad password")
                    )




    print parameters

    sendResponse(response, connection)

server(fridayWebapp)
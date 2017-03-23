# -*- coding: utf-8 -*-
import socketserver
from time import gmtime, strftime
from file import *
import json
import re
import time

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

clients = {} #loadusers("users.txt")
helpText = load("help.txt") #"List of commands: help, login, logout, msg, names, history"
history = [] #savehistory(history, "history.txt") # loadhistory("history.txt")
#loadusers("users.txt")

class ClientHandler(socketserver.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        
        # SKAL IKKE RETURNERE NOE #

        #connection, client_address = sock.accept()

        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.username = ""

        # Loop that listens for messages from the client
        while True:
            try:
                received_string = self.connection.recv(4096).decode()
            except Exception as e:
                print("Client has left, error:")
                print(e)
                time.sleep(3)

            if received_string:
                print("I got this request:", received_string)
                data = json.loads(received_string)
                req = data['request']

                if req == "login":
                    self.login(data['content'])
                    time.sleep(0.2)
                    self.history()
                elif req == "logout":
                    self.logout()
                elif req == "msg":
                    self.msg(data['content'])
                elif req == "names":
                    self.names()
                elif req == "history":
                    self.history()
                elif req == "help":
                    self.helptext()


    def login(self, username):
        try:
            # HUSK Å OPPDATERE LISTEN USERS
            if username not in clients and re.match("^[A-Za-z0-9_-]*$", username):

                if not self.isregistered(): #sjekker om self.connection eksisterer i clients
                    clients[username] = self.connection
                    self.username = username
                    #saveusers(clients, "users.txt")

                    self.connection.send(self.parse_info("Login successful! Welcome " + self.username + "!").encode())
                    self.broadcast(self.username + " logged in")
                else:
                    self.connection.send(self.parse_error("You are already logged in").encode())


            elif not re.match("^[A-Za-z0-9_-]*$", username):
                self.connection.send(self.parse_error("Username may only consist of letters and numbers").encode())
            elif username in clients:
                self.connection.send(self.parse_error("Username is taken").encode())
            else:
                self.connection.send(self.parse_error("Login failed").encode())
                
        except Exception as e:
            print(e)
            self.connection.send((self.parse_error("Error:" + e)))

    def isregistered(self):
        for username in clients:
            if clients[username] == self.connection:
                return True
        return False

    def msg(self, message):
        if self.username in clients:
            timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            #history.append("<" + timestamp + "> " + self.username + ": " + message)
            history.append({
                'timestamp': timestamp,
                'sender': self.username,
                'response': "message",
                'content': message
            })
            self.broadcast(message)
        else:
            self.connection.send(self.parse_error("User not logged in").encode())

    def logout(self):
        try:
            # HUSK Å OPPDATERE LISTEN USERS
            if self.username in clients:
                clients.pop(self.username)
                self.broadcast(self.username + " logged out")
                self.connection.send(self.parse_info("Logged out successfully").encode())
                self.username = ""
            else:
                self.connection.send(self.parse_error("Could not log out").encode())
        except Exception as e:
            print(e)
            print("Cannot find username in database")

    def helptext(self):
        text = "List of commands:\n"
        if self.username in clients:
            for line in helpText:
                text += "- " + line

            self.connection.send(self.parse_info(text).encode())
        else:
            for i in range(2):
                text += "- " + helpText[i]
            self.connection.send(self.parse_info(text).encode()) #"List of commands: help, login"

    def history(self):
        if self.username in clients:
            self.connection.send(self.parse_history().encode())
        else:
            self.connection.send(self.parse_error("User not logged in").encode())

    def names(self):
        if self.username in clients:
            # lager en liste over alle brukere (array)
            allUsers = []
            for i in clients.keys():
                allUsers.append(i)

            text = "List of users:\n"

            for i in range(len(allUsers)):
                text += "- " + allUsers[i] + "\n"

            self.connection.send(self.parse_info(text).encode())
        else:
            self.connection.send(self.parse_error("User not logged in").encode())

    def broadcast(self, message):
        for user in clients:
            clients[user].send(self.parse_msg(message).encode())

    def parse_msg(self, message):
        timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        return json.dumps({"timestamp": timestamp, "sender": self.username, "response": "message", "content": message})

    def parse_info(self, content):
        timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        return json.dumps({"timestamp": timestamp, "sender": "server", "response": "info", "content": content})

    def parse_error(self, error):
        timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        return json.dumps({"timestamp": timestamp, "sender": "server", "response": "error", "content": error}) 

    def parse_history(self):
        global history
        timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        return json.dumps({"timestamp": timestamp, "sender": "server", "response": "history", "content": history})

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """                                                      
    HOST, PORT = '192.168.43.37', 9998                       
    print('Server running...')                               
                                                             
    # Set up and initiate the TCP server                     
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)  
    server.serve_forever()                                   

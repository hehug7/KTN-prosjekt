# -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
import json
from time import sleep

#colors
class bcolors:
    PINK = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[93m'
    OKRED = '\033[91m'
    CYAN = '\033[96m'
    ENDC = '\033[0m'

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.server_port = server_port

        self.run()

    def disconnect(self):
        self.receiver.close()
        sleep(0.1)
        self.connection.close()
        print("Disconnecting")

    def receive_message(self, payload):
        try:
            #print("I got the payload!", payload) # json string
            payload = json.loads(payload)
            res = payload['response'] # the response
            content = payload['content'] #the content
            timestamp = payload['timestamp'] #the timestamp

            if res == "history":
                history = ""
                for client in content:
                    history += "<" + client['timestamp'] + "> " + client['sender'] + ": " + client['content'] + "\n"

                print("History:\n" + history)
            elif res == "names":
                print("<" + timestamp + "> " + content)
            elif res == "help":
                print("<" + timestamp + "> \n" + content)
            elif res == "message":
                print("<" + timestamp + "> " + payload['sender'] + ": " + content)
            elif res == "logout":
                print("<" + timestamp + "> " + content)

            else:
                print("<" + timestamp + "> " + content)

        except Exception as e:
            print(e)

    def send_payload(self, data):
        try:
            self.connection.send(data.encode()) # gjør string til binært
        except Exception as e:
            print("failed to send payload")
            print(e)

    def msg(self, payload):
        self.send_payload(json.dumps({"request": "msg", "content": payload}))

    def helptext(self):
        self.send_payload(json.dumps({"request": "help", "content": None}))

    def logout(self):
        self.send_payload(json.dumps({"request": "logout", "content": None}))

    def login(self, payload):
        self.send_payload(json.dumps({"request": "login", "content": payload}))

    def names(self):
        self.send_payload(json.dumps({"request": "names", "content": None}))

    def history(self):
        self.send_payload(json.dumps({"request": "history", "content": None}))

    def run(self):
        # Initiate the connection to the server

        try:
            self.connection.connect((self.host, self.server_port))
            print("connected")
        except Exception as i:
            print(i)
            print("Could not connect to host")
            exit()

        # Start messageParser
        self.parser = MessageParser()
        
        # Start messageReceiver
        self.receiver = MessageReceiver(self, self.connection)
        self.receiver.start()
        print("messageRec OK")

        while True:
            print("Write 'help' for list of commands.")
            userIn = input(">>> ")

            if userIn == "msg":
                message = input("Write your message: ")
                self.msg(message)

            elif userIn == "login":
                username = input("Username: ")
                self.login(username)

            elif userIn == "logout":
                self.logout()

            elif userIn == "names":
                self.names()

            elif userIn == "history":
                self.history()

            elif userIn == "help":
                self.helptext()
            elif userIn == "color":
                colors = ["red", "blue", "cyan", "green", "yellow", "pink"]
                colorCodes = ['\033[91m', '\033[94m', '\033[96m', '\033[92m', '\033[93m', '\033[95m']
                print("List of colors:\n- " + bcolors.OKGREEN + "green" + bcolors.ENDC + "\n- " + bcolors.OKBLUE + "blue" + bcolors.ENDC + "\n- " + bcolors.OKRED + "red" + bcolors.ENDC + "\n- " + bcolors.PINK + "pink" + bcolors.ENDC + "\n- " + bcolors.YELLOW + "yellow" + bcolors.ENDC + "\n- " + bcolors.CYAN + "cyan" + bcolors.ENDC)
                userColor = input("What color do you want? ")

                if userColor in colors:
                    for i in range(len(colors)):
                        if (userColor == colors[i]):
                            self.color = colorCodes[i]
                else:
                    print("Not a supported color...")

            elif userIn == "colors":
                print("\nTo be implemented; paint your username with following colors:")
                print(bcolors.OKGREEN + "green" + bcolors.ENDC)
                print(bcolors.OKBLUE + "blue" + bcolors.ENDC)
                print(bcolors.PINK + "pink" + bcolors.ENDC)
                print(bcolors.CYAN + "cyan" + bcolors.ENDC)
                print(bcolors.OKRED + "red" + bcolors.ENDC)
                print(bcolors.YELLOW + "yellow" + bcolors.ENDC)

            else:
                print("Not recognized command.")
                continue


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('91.192.223.73', 9998) #192.168.43.76 ruben # meg 192.168.43.37

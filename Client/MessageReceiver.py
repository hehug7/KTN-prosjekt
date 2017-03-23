# -*- coding: utf-8 -*-
from threading import Thread

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """
        Thread.__init__(self) # start thread

        # Flag to run thread as a deamon
        self.daemon = True
        self.client = client
        self.connection = connection
        self.closed = False

    def run(self):

        while True:
            try:
                data = self.connection.recv(4096).decode()
                if data:
                    self.client.receive_message(data)
                    #print("received data:", data)

            except ConnectionAbortedError:
                print("Connection aborted")

            if self.closed:
                break

    def close(self):
        self.closed = True


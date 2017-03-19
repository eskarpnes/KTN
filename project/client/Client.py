# -*- coding: utf-8 -*-
import socket
import json
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser


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
        self.username = None
        self.parser = MessageParser(self)
        self.connection.connect((self.host, self.server_port))
        self.receiver = MessageReceiver(self, self.connection)
        self.run()

    def run(self):
        while True:
            request = input()
            self.send_payload(request.split(" ", 1))

    def disconnect(self):
        self.connection.close()
        self.username = None
        print("Logout successful")

    def receive_message(self, message):
        self.parser.parse(message)

    def send_payload(self, data):
        if data[0].lower() == "login" and self.username is not None:
            print("You are already logged in")
            return None
        if data[0].lower() not in ["login", "logout", "msg", "names", "help"]:
            print(data[0].lower() + " is not a valid argument")
            return None
        if data[0].lower() in ["login", "msg"]:
            content = data[1]
        else:
            content = None
        payload = json.dumps({"request": data[0], "content": content})
        self.connection.send(payload.encode())


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)

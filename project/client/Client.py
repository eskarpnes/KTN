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
            if request == "quit":
                self.disconnect()
            self.send_payload(request.split(" ", 1))

    def disconnect(self):
        self.connection.close()
        quit()

    def logout(self):
        self.username = None
        print("Logout successful")

    def receive_message(self, message):
        self.parser.parse(message)

    def send_payload(self, data):
        payload = json.dumps({
                "request": data[0],
                "content": data[1] if data[0] in ["msg", "login"] else None
            })
        self.connection.send(payload.encode())


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)

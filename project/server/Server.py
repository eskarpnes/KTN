# -*- coding: utf-8 -*-
import socketserver
import json
import datetime
import re

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

connected_users = {}
message_history = []


def parse_payload(payload, handler):
    payload = json.loads(payload)
    if payload['request'].lower() in requests:
        requests[payload['request'].lower()](payload, handler)
    else:
        handler.send(send_error("Not a valid request"))


def login(payload, handler):
    username = payload["content"]
    if handler.username is None:
        if not username.isalnum():
            handler.send(send_error("Not a valid username"))
            return
        if username in connected_users.keys():
            handler.send(send_error("The username is taken"))
        else:
            handler.username = username
            connected_users[username] = handler
            handler.send(send_info("Welcome " + username))
            send_history(handler)
    else:
        handler.send(send_error("You are already logged in"))


def logout(payload, handler):
    if handler.username is None:
        handler.send(send_error("You must log in first"))
        return
    connected_users.pop(handler.username)
    handler.username = None
    handler.send(send_info("Logout successful"))
    #handler.kill()


def msg(payload, handler):
    if handler.username is None:
        handler.send(send_error("You must log in first"))
        return
    content = payload["content"]
    message = {
        "timestamp": '{:%x - %X}'.format(datetime.datetime.now()),
        "sender": handler.username,
        "response": "message",
        "content": content
    }
    payload = json.dumps(message)
    message_history.append(payload)
    for user, handler in connected_users.items():
        handler.send(payload.encode())

    handler.send(send_info("Message delivered"))


def names(payload, handler):
    if handler.username is None:
        handler.send(send_error("You must log in first"))
        return
    connected = "\n".join(list(connected_users.keys()))
    message = {
        "timestamp": '{:%x - %X}'.format(datetime.datetime.now()),
        "sender": "server",
        "response": "names",
        "content": connected
    }
    payload = json.dumps(message)
    handler.send(payload.encode())


def help(payload, handler):
    content = "Available commands:\nlogin <username>  - log in with the given username \nlogout    - log out \nmsg" \
              " <message>  - send message\nnames    - list users in chat \nhelp    - view help text"
    message = {
        "timestamp": '{:%x - %X}'.format(datetime.datetime.now()),
        "sender": "server",
        "response": "info",
        "content": content
    }
    payload = json.dumps(message)
    handler.send(payload.encode())


def send_info(content):
    message = {
        "timestamp": '{:%x - %X}'.format(datetime.datetime.now()),
        "sender": "server",
        "response": "info",
        "content": content
    }
    payload = json.dumps(message)
    return payload.encode()


def send_error(content):
    message = {
        "timestamp": '{:%x - %X}'.format(datetime.datetime.now()),
        "sender": "server",
        "response": "error",
        "content": content
    }
    payload = json.dumps(message)
    return payload.encode()


def send_history(handler):
    payload = {
        "timestamp": '{:%x - %X}'.format(datetime.datetime.now()),
        "sender": "server",
        "response": "history",
        "content": "This is the history of the chatroom"
    }
    payload = json.dumps(payload)
    handler.send(payload.encode())
    for message in message_history:
        payload = {
            "timestamp": message["timestamp"],
            "sender": message["sender"],
            "response": "history",
            "content": message["content"]
        }
        payload = json.dumps(payload)
        handler.send(payload.encode())


requests = {
    "login": login,
    "logout": logout,
    "msg": msg,
    "names": names,
    "help": help,
}


class ClientHandler(socketserver.BaseRequestHandler):
    """
    This is the ClientHandler class. Every time a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.username = None

        # Loop that listens for messages from the client
        while True:
            received_string = self.connection.recv(4096)
            # TODO: Add handling of received payload from client
            parse_payload(received_string.decode(), self)

    def send(self, payload):
        self.connection.send(payload)

    def disconnect(self):
        print("Killing thread")
        self.connection.close()


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
    HOST, PORT = '10.22.44.60', 9998
    print('Server running...')

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()

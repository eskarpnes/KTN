# -*- coding: utf-8 -*-
import socketserver
import json
import datetime

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

connected_users = {}
message_history = []


def parse_payload(payload, handler):
    payload = json.loads(payload)
    return requests[payload['request']](payload, handler)


def login(payload, handler):
    username = payload["content"]
    if username in connected_users.keys():
        handler.send(send_error("The username is taken"))
    else:
        handler.username = username
        connected_users[username] = handler
        handler.send(send_info("Welcome " + username))


def logout(payload, handler):
    connected_users.pop(handler.username)
    handler.send(send_info("Logout successful"))
    handler.kill()

def msg(payload, handler):
    content = payload["content"]
    message = {
        "timestamp": str(datetime.datetime.utcnow()),
        "sender": handler.username,
        "response": "message",
        "content": content
    }
    payload = json.dumps(message)
    message_history.append(payload)
    for user, handler in connected_users.items():
        handler.send(payload.encode())

    return send_info("Message delivered")


def names(payload, handler):
    connected = "/n".join(list(connected_users.keys()))
    message = {
        "timestamp": str(datetime.datetime.utcnow()),
        "sender": "server",
        "response": "names",
        "content": connected
    }
    payload = json.dumps(message)
    handler.send(payload.encode())


def help():
    pass


def send_info(content):
    message = {
        "timestamp": str(datetime.datetime.utcnow()),
        "sender": "server",
        "response": "info",
        "content": content
    }
    payload = json.dumps(message)
    return payload.encode()


def send_error(content):
    message = {
        "timestamp": str(datetime.datetime.utcnow()),
        "sender": "server",
        "response": "error",
        "content": content
    }
    payload = json.dumps(message)
    return payload.encode()

def send_history():
    message = {
        "timestamp": str(datetime.datetime.utcnow()),
        "sender": "server",
        "response": "history",
        "content": message_history
    }

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

    def kill(self):
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
    HOST, PORT = 'localhost', 9998
    print('Server running...')

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
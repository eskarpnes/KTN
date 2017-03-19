import json


class MessageParser():
    def __init__(self, client):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message': self.parse_message,
            'history': self.parse_history,
            'names': self.parse_names
        }

        self.client = client

    def parse(self, payload):
        payload = json.loads(payload.decode())
        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            print("You have met a terrible fate...")

    def parse_error(self, payload):
        timestamp = payload["timestamp"]
        message = payload["content"]
        sender = payload["sender"]
        print("Sender: " + sender + "   " + timestamp)
        print(message)

    def parse_info(self, payload):
        if payload["content"] == "Logout successful":
            self.client.disconnect()
        if payload["content"][:7] == "Welcome":
            self.client.username = payload["content"][8:]

    def parse_message(self, payload):
        timestamp = payload["timestamp"]
        message = payload["content"]
        sender = payload["sender"]
        print("Sender: " + sender + "   " + timestamp)
        print(message)
        print("")

    def parse_history(self, payload):
        messages = payload["content"]
        for message in messages:
            self.parse_message(json.loads(message))

    def parse_names(self, payload):
        print(payload["content"])

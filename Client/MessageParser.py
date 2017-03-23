import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'msg': self.parse_msg,
            'history': self.parse_history
        }

    def parse(self, payload):
        payload = json.loads(payload) # decode JSON object

        if payload['response'] in self.possible_responses:
            return self.possible_responses[payload['response']](payload)
        else:
            print("Not valid response")
            return self.possible_responses['error'](payload)

    def parse_error(self, payload):
        return "<" + payload.get('timestamp') + "> Error: " + payload.get('content')

    def parse_info(self, payload):
        return "<" + payload.get('timestamp') + "> Info: " + payload.get('content')

    def parse_msg(self, payload):
        return "<" + payload.get('timestamp') + "> Message: " + payload.get('content')

    def parse_history(self, payload):
        return "<" + payload.get('timestamp') + "> History: " + payload.get('content')

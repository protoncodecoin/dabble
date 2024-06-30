from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class chatConsumer(WebsocketConsumer):

    def connect(self):
        """
        Establish connection with the client
        """
        self.accept()

    def receive(self, text_data):
        """
        Receives message sent from client
        """
        print(text_data)

    def messenger(self, message):
        print(message)

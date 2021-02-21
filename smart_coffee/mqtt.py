"""
This modules handles abtracting the MQTT communication logic.
"""
import paho.mqtt.client as mqtt
from typing import Callable


def _on_message_handler(client, callback_dict, message):
    """
    Message handler that takes in the message and redirects the handling to
    various callback functions that may be subscribed.
    """
    # If the message topic is in the subscribed list, handle it
    if message.topic in callback_dict:
        callback_dict[message.topic](message)


class MQTTClient:
    """
    Represents the client which is used for communicating over MQTT
    """
    def __init__(self, hostname: str, port: int):
        """
        Create a new MQTT connection on the given hostname and port

        :param hostname: The hostname of the MQTT broker
        :type hostname: str
        :param port: The port to connect to
        :type port: int
        """
        # Create a dictionary of topics and callbacks
        self.callback_dict = dict()

        self.client = mqtt.Client(userdata=self.callback_dict)
        self.client.on_message = _on_message_handler
        self.client.connect(hostname, port, 20)
        
    def subscribe(self, topic: str, call_back):
        """
        Subscribe to a given topic in which each time the topic is posted to,
        the given call back which takes in a message is called.

        :param topic: The topic to subscribe to
        :type topic: str

        """
        self.callback_dict[topic] = call_back
        self.client.subscribe(topic)
 
    def loop_forever(self):
        """
        Handles blocking and keeping the program looping and waiting for
        MQTT messages.
        """
        self.client.loop_forever()

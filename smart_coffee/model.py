from enum import Enum
import parse
import abc


class MQTTMessage:
    """
    Represents the messages that are sent back and forth through MQTT.
    """

    def __init__(self, topic: str):
        """
        Create a new MQTT message with a given topic

        :param topic: The topic of the MQTT message
        :type topic: str
        """
        self.topic = topic

    @abc.abstractmethod
    def get_payload(self) -> bytes:
        """
        Get the payload of the message as bytes.

        :return: Byte representation of the payload
        :rtype: bytes
        """
        raise NotImplementedError

    @abc.abstractmethod
    def parse_message(payload: bytes):
        """
        Handles parsing the payload to a message.

        :param payload: The bytes to parse
        :type payload: bytes
        """
        raise NotImplementedError

class CoffeeState(Enum):
    """
    Represents the state that the coffee maker could be in. The state
    represents the immediate state of the coffee maker.
    """
    ON = 1
    OFF = 2


class CoffeeStateMessage(MQTTMessage):
    """
    Represents the MQTT message that is used to set the state of the coffee
    maker.
    """
    _message_format = 'state = {coffee_state}'
    _message_topic = 'coffee/state'

    def __init__(self, coffee_state: CoffeeState):
        """
        Create a message that is used for setting the state of the coffee maker
        
        :param coffee_state: The state to set the coffee maker to
        """
        super().__init__(self._message_topic)
        self.coffee_state = coffee_state

    def get_payload(self) -> bytes:
        """
        Get the payload of the message that can be sent as an MQTT payload

        :return: The bytes representation of the payload
        :rtype: bytes
        """
        encoded_str = _message_format.format(coffee_state=self.coffe_state.value)
        return bytes(encoded_str, 'utf-8')

    @classmethod
    def parse_message(cls, payload: bytes):
        """
        Parses an MQTT message into a coffee state message

        :param payload: The payload to parse
        :type payload: bytes
        :return: The parsed message of the coffee state
        """
        payload_str = payload.decode('utf-8')
        state = parse.parse(cls._message_format, payload_str)['coffee_state']
        return CoffeeStateMessage(CoffeeState[state])

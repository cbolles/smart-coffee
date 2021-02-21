import gpiozero as gpio
import paho.mqtt.client as mqtt
import model

coffee_maker = gpio.LED(4)

def on_mqtt_connect(client, userdata, flags, rc):
    """
    Handles setting the initial setup of the MQTT connection including
    subscribing to the necessary topics.
    """
    client.subscribe('coffee/#')


def on_mqtt_message(client, userdata, message):
    """
    Handles in comming messages related to the MQTT topics that have been
    subscribed to.
    """
    # Handle turning coffee machine on / off
    if message.topic == 'coffee/state':
        coffee_message = model.CoffeeStateMessage.parse_message(message.payload)
        if coffee_message.coffee_state == model.CoffeeState.ON:
            coffee_maker.on()
        else:
            coffee_maker.off()
    # Handle setting up a time to turn on the coffe maker
    elif message.topic == 'coffee/time':
        pass
    print(message.topic + ': ' + str(message.payload))


if __name__ == '__main__':

    # Setup MQTT
    client = mqtt.Client()
    client.on_connect = on_mqtt_connect
    client.on_message = on_mqtt_message

    # Connect to MQTT and loop forever
    client.connect("10.2.75.239", 1883, 20)
    client.loop_forever()

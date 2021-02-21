import gpiozero as gpio
import paho.mqtt.client as mqtt
import model
import mqtt

coffee_maker = gpio.LED(4)

def on_set_state(message):
    """
    Handles setting the state of the coffee maker

    :param message: The MQTT message containing the state information
    """
    coffee_message = model.CoffeeStateMessage.parse_message(message.payload)
    if coffee_message.coffee_state == model.CoffeeState.ON:
        coffee_maker.on()
        print('Coffee maker on')
    else:
        coffee_maker.off()
        print('Coffee maker off')


if __name__ == '__main__':
    mqtt_client = mqtt.MQTTClient("10.2.75.239", 1883)
    mqtt_client.subscribe("coffee/state", on_set_state)
    mqtt_client.loop_forever()

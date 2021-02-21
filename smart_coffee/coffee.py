import gpiozero as gpio
import paho.mqtt.client as mqtt
import model
import mqtt
from threading import Timer
from time import time


# TOTAL_BREWINING_TIME_SECONDS = 390
TOTAL_BREWINING_TIME_SECONDS = 30

coffee_maker = gpio.LED(4)
mqtt_client = mqtt.MQTTClient("10.2.75.239", 1883)

def send_finished():
    """
    Sends the finished brewining message and stops the brewing process after
    the brewing has completed.
    """
    def stop():
        coffee_maker.off()
        status = model.CoffeeStatusMessage(model.CoffeeStatus.FINISHED)
        mqtt_client.publish(status)
        print('Brewining finished')
    timer = Timer(TOTAL_BREWINING_TIME_SECONDS, stop)
    timer.start()


def on_set_state(message):
    """
    Handles setting the state of the coffee maker

    :param message: The MQTT message containing the state information
    """
    coffee_message = model.CoffeeStateMessage.parse_message(message.payload)
    if coffee_message.coffee_state == model.CoffeeState.ON:
        coffee_maker.on()
        print('Coffee maker on')
        send_finished()
    else:
        coffee_maker.off()
        print('Coffee maker off')


def on_set_timer(message):
    """
    Handles setting a timer for starting the coffee

    :param message: The MQTT message containing the timer information
    """
    timer_message = model.CoffeeTimerMessage.parse_message(message.payload)

    def start_coffee():
        print('Making coffee')
        coffee_maker.on()
        send_finished()

    delta_time = timer_message.timestamp - time()
    timer = Timer(delta_time, start_coffee)
    timer.start()


if __name__ == '__main__':
    # Subscribe to messages
    mqtt_client.subscribe("coffee/state", on_set_state)
    mqtt_client.subscribe("coffee/time", on_set_timer)

    mqtt_client.loop_forever()

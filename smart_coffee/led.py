import gpiozero as gpio
import model
import mqtt
import time


coffee_indicator = gpio.LED(4)
mqtt_client = mqtt.MQTTClient("10.2.75.239", 1883)


def indicate_coffee_done(message):
    """
    Handles flashing the LED to indicate that the coffee is ready 
    """
    for i in range(0, 5):
        coffee_indicator.on()
        time.sleep(0.5)
        coffee_indicator.off()
        time.sleep(0.5)


if __name__ == '__main__':
    mqtt_client.subscribe('coffee/status', indicate_coffee_done)
    mqtt_client.loop_forever()

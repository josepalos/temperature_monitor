import asyncio
import time
import json

import websockets
import RPi.GPIO as GPIO



WS_URL = "ws://192.168.137.145:8000/ws/notifications/"

TOO_COLD = 0
TOO_COLD_PIN = 13
NORMAL = 1
NORMAL_PIN = 6
TOO_HOT = 2
TOO_HOT_PIN = 5


def set_pins(notification_type):
    if notification_type == TOO_COLD:
        GPIO.output(TOO_COLD_PIN, GPIO.HIGH)
        GPIO.output(NORMAL_PIN, GPIO.LOW)
        GPIO.output(TOO_HOT_PIN, GPIO.LOW)
    elif notification_type == TOO_COLD:
        GPIO.output(TOO_COLD_PIN, GPIO.LOW)
        GPIO.output(NORMAL_PIN, GPIO.HIGH)
        GPIO.output(TOO_HOT_PIN, GPIO.LOW)
    else:
        GPIO.output(TOO_COLD_PIN, GPIO.LOW)
        GPIO.output(NORMAL_PIN, GPIO.LOW)
        GPIO.output(TOO_HOT_PIN, GPIO.HIGH)

async def parse_message(message):
    message = json.loads(message)
    message = message["notification"]
    text = message["message"]
    print(text)
    notification_type = message["type"]
    set_pins(notification_type)


async def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TOO_COLD_PIN, GPIO.OUT)
    GPIO.setup(NORMAL_PIN, GPIO.OUT)
    GPIO.setup(TOO_HOT_PIN, GPIO.OUT)
    print("Init pins")
    set_pins(NORMAL)


    async with websockets.connect(WS_URL) as ws:
        print("Connected")
        async for message in ws:
            await parse_message(message)


if __name__ == "__main__":
    while True:
        try:
            asyncio.get_event_loop().run_until_complete(main())
            main()
        except KeyboardInterrupt:
            GPIO.cleanup()
            break
        except Exception as ex:
            print(ex)
            time.sleep(5)
            continue


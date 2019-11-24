import asyncio
import websockets
import RPi.GPIO as GPIO



WS_URL = "ws://192.168.137.145:8000/ws/notifications/"

TOO_COLD = 0
TOO_COLD_PIN = 13
NORMAL = 1
NORMAL_PIN = 6
TOO_HOT = 2
TOO_HOT_PIN = 5


async def parse_message(message):
    text = message["message"]
    notification_type = message["type"]
    print(message)
    if notification_type == TOO_COLD:
        GPIO.output(TOO_COLD, GPIO.HIGH)
        GPIO.output(NORMAL, GPIO.LOW)
        GPIO.output(TOO_HOT_PIN, GPIO.LOW)
    elif notification_type == TOO_COLD:
        GPIO.output(TOO_COLD, GPIO.LOW)
        GPIO.output(NORMAL, GPIO.HIGH)
        GPIO.output(TOO_HOT_PIN, GPIO.LOW)
    elif notification_type == TOO_COLD:
        GPIO.output(TOO_COLD, GPIO.LOW)
        GPIO.output(NORMAL, GPIO.LOW)
        GPIO.output(TOO_HOT_PIN, GPIO.HIGH)


async def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TOO_COLD_PIN, GPIO.OUT)
    GPIO.setup(NORMAL_PIN, GPIO.OUT)
    GPIO.setup(TOO_HOT_PIN, GPIO.OUT)


    async with websockets.connect(WS_URL) as ws:
        async for message in ws:
            await parse_message(message)


if __name__ == "__main__":
    while True:
        try:
            asyncio.get_event_loop().run_until_complete(main())
            main()
        except KeyboardException:
            GPIO.cleanup()
            break
        except Exception:
            continue


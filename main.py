print("IoT Gateway")
import sys
# import random
import time
import serial.tools.list_ports
from Adafruit_IO import MQTTClient

AIO_FEED_IDS = ["vgu-led", "vgu-led-2", "vgu-temperature", "vgu-light", "air-humid", "air-temp", "soil-mois"]
AIO_USERNAME = "khoikieu1608"
AIO_KEY = "aio_ORpa061KlKGzMAjZhsFl7KGLG4n1"

def connected(client):
    print("Connect Successfully ...")
    for feed in AIO_FEED_IDS:
        client.subscribe(feed)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribed  ...")

def disconnected(client):
    print("Disconnected ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Received Message: " + payload)
    print("Received data from feed_id: " + feed_id)
    if isMicrobitConnected:
        ser.write((str(payload) + "#").encode())

client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort

print("Testing port:", getPort())

isMicrobitConnected = False
if getPort() != "None":
    ser = serial.Serial(port=getPort(), baudrate=115200)
    print("MCU is connected!!!")

mess = ""
def processData(data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    if splitData[1] == "TEMP":
        client.publish("vgu-temperature", splitData[2])
    if splitData[1] == "LIGHT":
        client.publish("vgu-light", splitData[2])
    if splitData[1] == "AIR-TEMP":
        client.publish("air-temp", splitData[2])
    if splitData[1] == "AIR-HUMID":
        client.publish("air-humid", splitData[2])
    if splitData[1] == "SOIL-MOIS":
        client.publish("soil-mois", splitData[2])

def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]


counter = 0
while True:
    # counter = counter + 1
    # if counter >= 30:
    #     value = random.randint(25, 55)
    #     client.publish("vgu-led", value)
    #     print("Data is published:", value)
    #     counter = 0
    if isMicrobitConnected:
        readSerial()
    time.sleep(1)
    pass
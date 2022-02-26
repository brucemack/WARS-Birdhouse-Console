import serial
import time
import json
from datetime import datetime

# Open the serial port
ser = serial.Serial('COM5', 115200, timeout=0.1)
# Open the text file
log = open("./ping.csv","a")

last_ping_time = 0
ping_interval_seconds = 10
ping_node = 3

# Sample loop result
while True:

    # Send ping if necessary
    if (time.time() - last_ping_time) >= ping_interval_seconds:
        last_ping_time = time.time()
        # Send ping
        ser.write(("ping " + str(ping_node) +"\r").encode())

    # Process results, look for PONG
    try:
        raw_line = ser.readline()
        if len(raw_line) == 0:
            continue
        line = raw_line.decode().strip()
    except:
        continue    

    if line.startswith("PONG: "):
        # Parse JSON
        data = json.loads(line[6:])
        print(data)

        my_date = datetime.now()
        log.write(my_date.strftime("%Y-%m-%d %H:%M:%S"))
        log.write(",")
        log.write(str(data["originalSourceAddr"]))
        log.write(",")
        log.write(str(data["batteryMv"]))
        log.write(",")
        log.write(str(data["panelMv"]))
        log.write(",")
        log.write(str(data["receiveRssi"]))
        log.write(",")
        log.write(str(data["uptimeSeconds"]))
        log.write(",")
        log.write(str(data["bootCount"]))
        log.write("\n")
        log.flush()

ser.close()             # close port
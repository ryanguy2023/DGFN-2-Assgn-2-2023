import socket
import os
import json

s = socket.socket()
host = '10.102.13.82'  # Localhost
port = 5000
s.bind((host, port))
s.listen(5)


#this function is respolsible for getting Data from the core like temp and voltage
def get_core_data():
    temperature_str = os.popen('vcgencmd measure_temp').readline() #got from https://www.nicm.dev/vcgencmd/
    temperature = float(temperature_str.replace("temp=", "").replace("'C\n", ""))

    corevolt_str = os.popen('vcgencmd measure_volts').readline() #got from https://www.nicm.dev/vcgencmd/
    core_voltage = float(corevolt_str.split('=')[1].replace("V\n", ""))

    return {"Temperature": temperature, "Core Voltage": core_voltage}


#this function is respolsible for getting the clock speeds for the Arm and pixel.
def get_clock_speeds():
    arm_clock_str = os.popen('vcgencmd measure_clock arm').readline() #got from https://www.nicm.dev/vcgencmd/
    pixel_clock_str = os.popen('vcgencmd measure_clock pixel').readline() #got from https://www.nicm.dev/vcgencmd/

    # Extracting the clock speeds from the strings
    arm_clock_speed = int(arm_clock_str.split('=')[1])
    pixel_clock_speed = int(pixel_clock_str.split('=')[1])

    return {"Arm Clock Speed": arm_clock_speed, "Pixel Clock Speed": pixel_clock_speed}

while True:
    c, addr = s.accept()
    print('Got connection from', addr)

    # Get data from the functions (temperature, voltage, and clock speeds)
    core_data = get_core_data()
    clock_speeds = get_clock_speeds()

    # Combine data into a single dictionary
    all_data = {**core_data, **clock_speeds}

    # Convert data to JSON
    json_data = json.dumps(all_data)

    # Convert JSON to bytes
    response = bytes(json_data, 'utf-8')

    c.sendall(response)  # Use sendall to ensure the entire message is sent
    c.close()


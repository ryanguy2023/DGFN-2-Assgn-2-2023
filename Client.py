import socket
import json
from time import sleep as sl

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('10.102.13.82', 5000))  # Connects to the server, update port if necessary

for i in range(10):
    # Receive and print the data
    received_data = s.recv(1024)

    if not received_data:
        print("No data received. Exiting.")
        break

    # Decode the received data
    decoded_data = received_data.decode('utf-8')

    try:
        # Parse the JSON data
        data_dict = json.loads(decoded_data)

        # Print each piece of information separately on a new line
        print("Received data:")
        for key, value in data_dict.items():
            print(f"    {key}: {value}")

    except json.decoder.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Received data: {decoded_data}")

    sl(1)

print("All done")


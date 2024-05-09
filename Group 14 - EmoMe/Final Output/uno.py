import serial
import time

# Replace 'COMX' with the actual port of your Arduino
arduino = serial.Serial('COM10', 9600)

def send_value(value):
    arduino.write(str(value).encode())  # Send the value to Arduino
    time.sleep(0.1)  # Wait for stability

try:
    while True:
        # Read the value from a text file
        with open('greatest_position.txt', 'r') as file:
            value = int(file.read().strip())
            send_value(value)  # Send the value to Arduino
            print(f"Sent value: {value}")
        time.sleep(1)  # Wait for 1 second before checking again
except KeyboardInterrupt:
    arduino.close()  # Close the serial connection when the script is interrupted

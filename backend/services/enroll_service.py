import serial
import time

# Define serial port settings
port = 'COM16'
baudrate = 57600
timeout = 1  # Adjust timeout as needed

# Initialize serial connection
ser = serial.Serial(port, baudrate, timeout=timeout)

def send_command(command):
    # Send command to the sensor
    ser.write(command)
    time.sleep(0.1)  # Wait for the response
    response = ser.read_all()  # Read response
    return response

def main():
    # Example commands
    # Replace these with the actual commands you want to send
    print("Put Your Finger on Sensor")
    time.sleep(2)
    commands = [
        b'\x01\x00\x00\x00\x00\x01\x00\x00\x07\x13\x00\x00\x00\x00\x00\x1b',
        # Example command to verify password
        b'\x01\x00\x00\x00\x00\x03\x00\x00\x04\x01\x00\x00\x00\x00\x08\xfb\x26'
    ]

    for command in commands:
        response = send_command(command)
        print("Command:", command)
        print("Response:", response)

    # Close serial connection
    ser.close()
    print("FingerPrint Enrolled")

if __name__ == "__main__":
    main()

import pylsl
import serial
import time

# Connect to the serial port
ser = serial.Serial('COM9', 9600)
time.sleep(2)

# Resolve the LSL stream
print("Looking for an EEG stream...")
streams = pylsl.resolve_stream('type', 'Markers')

# Create a new inlet to receive the stream
inlet = pylsl.stream_inlet(streams[0])

while True:
    # Get the next sample from the stream
    sample, timestamp = inlet.pull_sample()
    marker = sample[0]
    print("Marker:", marker)

    # Send the appropriate serial command based on the marker value
    if marker == 1:
        print("Closing...")
        ser.write(b'H')
    elif marker == 2:
        print("Opening...")
        ser.write(b'L')
    else:
        print("Unknown marker value:", marker)

import pylsl
import serial
# Open serial port
ser = serial.Serial('COM9', 9600) 
# Resolve EEG stream on the lab network
streams = pylsl.resolve_byprop('type', 'Markers', timeout=2)
if not streams:
    print("No streams found with type 'Markers'")
else:
    # Create a new inlet to read from the stream
    inlet = pylsl.stream_inlet(streams[0])
    # Declare variables to count the number of left and right markers
    left_count = 0
    right_count = 0
    # Loop to match the marker name with the label and count repetitions
    while True:
        sample, timestamp = inlet.pull_sample()

        if sample[0] == 770:
            left_count += 1
            # Send the label to the Arduino
            ser.write(b'L') 
        elif sample[0] == 769:
            right_count += 1
            ser.write(b'R') 
        else:
            print("Unknown marker")
        # Print the number of repetitions of each label
        print("Left: %d, Right: %d" % (left_count, right_count))







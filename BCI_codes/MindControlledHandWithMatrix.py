import pylsl
import serial

# Open serial port
ser = serial.Serial('COM5', 9600)

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

    # Variables for storing information
    info_matrix = []  # Matrix to store marker information
    matrix_size = 15   # Number of samples to store in the matrix

    while True:
        sample, timestamp = inlet.pull_sample()

        if sample[0] == 770:
            left_count += 1
            info_matrix.append(sample[0])

            # If the matrix is full, calculate the average and send the signal
            if len(info_matrix) == matrix_size:
                average = sum(info_matrix) / matrix_size

                if average == 770:
                    ser.write(b'O')
                else:
                    print("Unknown marker")

                info_matrix = []  # Clear the matrix after sending the signal

        elif sample[0] == 769:
            right_count += 1
            info_matrix.append(sample[0])

            # If the matrix is full, calculate the average and send the signal
            if len(info_matrix) == matrix_size:
                average = sum(info_matrix) / matrix_size

                if average == 769:
                    ser.write(b'C')
                else:
                    print("Unknown marker")

                info_matrix = []  # Clear the matrix after sending the signal

        else:
            print("Unknown marker")

        # Print the number of repetitions of each label
        print("Left: %d, Right: %d" % (left_count, right_count))

from matplotlib import pyplot as plt
import numpy as np
import pylsl
import serial
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

# Open serial port
ser = serial.Serial('COM5', 9600)

# Resolve EEG stream on the lab network
streams = pylsl.resolve_byprop('type', 'Markers', timeout=2)

if not streams:
    print("No streams found with type 'Markers'")
else:
    # Create a new inlet to read from the stream
    inlet = pylsl.stream_inlet(streams[0])

    # Variables for storing information
    infoMatrix = []  # Matrix to store marker information
    matrixSize = 17  # Number of samples to store in the matrix
    closeCount = 0  # Count of left markers
    openCount = 0  # Count of right markers
    closeSamples = []  # List to store "close" samples
    openSamples = []  # List to store "open" samples
    repeticiones_770 = 0  # Counter for consecutive repetitions of 770
    repeticiones_769 = 0  # Counter for consecutive repetitions of 769

    while True:
        sample, timestamp = inlet.pull_sample()

        if sample[0] == 770:
            closeCount += 1
            infoMatrix.append(sample[0])
            repeticiones_770 += 1
            repeticiones_769 = 0  # Reset the counter for 769 repetitions

            if repeticiones_770 == 3:  # If 770 is repeated 3 times consecutively
                sample[0] = 769  # Change 770 to 769
                repeticiones_770 = 0  # Reset the counter for 770 repetitions

            # If the matrix is full, calculate the average and send the signal
            if len(infoMatrix) == matrixSize:
                average = sum(infoMatrix) / matrixSize

                if average == 770:
                    ser.write(b'O')
                else:
                    print("Abrir")

                infoMatrix = []  # Clear the matrix after sending the signal

        elif sample[0] == 769:
            openCount += 1
            infoMatrix.append(sample[0])
            repeticiones_769 += 1
            repeticiones_770 = 0  # Reset the counter for 770 repetitions

            if repeticiones_769 == 3:  # If 769 is repeated 3 times consecutively
                sample[0] = 770  # Change 769 to 770
                repeticiones_769 = 0  # Reset the counter for 769 repetitions

            # If the matrix is full, calculate the average and send the signal
            if len(infoMatrix) == matrixSize:
                average = sum(infoMatrix) / matrixSize

                if average == 769:
                    ser.write(b'C')
                else:
                    print("Cerrar")

                infoMatrix = []  # Clear the matrix after sending the signal

        else:
            print("Unknown marker")

        # Check if the matrix is full and print the counts
        if len(infoMatrix) == matrixSize:
            print("Close: %d, Open: %d" % (closeCount, openCount))

        # Rest of the code...
        # Rest of the code...
        if len(closeSamples) >= 2 and len(openSamples) >= 2:
            X = np.concatenate((closeSamples, openSamples))
            y = np.concatenate((np.zeros(len(closeSamples)), np.ones(len(openSamples))))

            lda = LinearDiscriminantAnalysis(n_components=2)
            X_lda = lda.fit_transform(X, y)

            plt.scatter(X_lda[:, 0], X_lda[:, 1], c=y, cmap='viridis')
            plt.xlabel('LDA Component 1')
            plt.ylabel('LDA Component 2')
            plt.title('LDA Visualization')
            plt.show()


           

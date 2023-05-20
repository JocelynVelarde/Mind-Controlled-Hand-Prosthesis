import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import matplotlib.pyplot as plt
import pylsl
import serial

# Open serial port
#ser = serial.Serial('COM9', 9600) 

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
    X = []
    y = []
    # Loop to match the marker name with the label and count repetitions
    while True:
        sample, timestamp = inlet.pull_sample()

        if sample[0] == 770:
            left_count += 1
            X.append([timestamp])
            y.append(0)
            # Send the label to the Arduino
           # ser.write(b'L') 
        elif sample[0] == 769:
            right_count += 1
            X.append([timestamp])
            y.append(1)
          #  ser.write(b'R') 
        else:
            print("Unknown marker")
        # Print the number of repetitions of each label
        print("Left: %d, Right: %d" % (left_count, right_count))
        
X = np.array(X)
y = np.array(y)

# Generate sample data
np.random.seed(0)
n_samples = len(X)
n_features = 1

# Initialize and fit the model
lda = LinearDiscriminantAnalysis(n_components=1)
X_r2 = lda.fit(X, y).transform(X)

plt.figure(figsize=(15, 8))
# Plotting the graph
plt.scatter(X_r2[:,0], X_r2[:,0], c=y)
plt.show()

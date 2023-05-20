# importing the module
from sklearn import datasets
# loading the iris data
dataset  = datasets.load_iris()

print(dataset['DESCR'])

import pandas as pd
# convertig the dataset into pandas dataframe
data = pd.DataFrame(dataset.data, columns=dataset.feature_names)
# descriptive statistics
data.describe()

X = dataset.data
y = dataset.target
target_names = dataset.target_names
# importing the requried module
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
# initializing the model with 2 components
lda = LinearDiscriminantAnalysis(n_components=2)
# fitting the dataset
X_r2 = lda.fit(X, y).transform(X)

import matplotlib.pyplot as plt
# plot size
plt.figure(figsize=(15, 8))
# plotting the graph
plt.scatter(X_r2[:,0],X_r2[:,1],  c=dataset.target)
plt.show()
# This elbow curve algorithm is used to identify the amount of clusters needed for clustering algorithms
# libraries needed
from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from common.path_to_use import *

# data file
# df = '/Users/Jeswanth/Desktop/rpDf.csv'
df = pd.read_csv(getOEMConcatData())
df = pd.read_csv(df, usecols=['downPayment', 'recurringPayment', 'brand']).dropna()

# Creating the data
x1 = df[['downPayment']].values
x2 = df[['recurringPayment']].values
X = np.array(list(zip(x1, x2))).reshape(len(x1), 2)

# This creates empty arrays and dfs
distortions = []
inertias = []
mapping1 = {}
mapping2 = {}
K = range(1, 10)
# This allows to see the range of K

for k in K:
    # This is the algorithm for building and fitting the model
    kmeanModel = KMeans(n_clusters=k).fit(X)
    kmeanModel.fit(X)

    distortions.append(sum(np.min(cdist(X, kmeanModel.cluster_centers_,
                                        'euclidean'), axis=1)) / X.shape[0])
    inertias.append(kmeanModel.inertia_)

    mapping1[k] = sum(np.min(cdist(X, kmeanModel.cluster_centers_,
                                   'euclidean'), axis=1)) / X.shape[0]
    mapping2[k] = kmeanModel.inertia_

for key, val in mapping1.items():
    print(str(key) + ' : ' + str(val))

plt.plot(K, distortions, 'bx-')
plt.xlabel('Values of K')
plt.ylabel('Distortion')
plt.title('The Elbow Method using Distortion')
plt.show()
# This is the organization to define the parameters for the plot.



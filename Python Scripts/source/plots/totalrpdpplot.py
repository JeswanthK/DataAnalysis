# This plot allows you to see all clusters in a totality to see how the clusters work on all the data
# Libraries needed
import pandas as pd
import seaborn
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cdist
import numpy as np

# figure options
plt.rcParams['figure.figsize'] = (20, 7.5)
# Other
import warnings

warnings.filterwarnings("ignore")
#from common.path_to_use import *

# data File
label_encoder = preprocessing.LabelEncoder()
segment_dict = {}
data = pd.read_csv('/Users/Jeswanth/Desktop/Sky 12:2/OEM.csv')
#data = pd.read_csv(getOEMConcatData())
new_df = data.filter(items=['brand', 'segment', 'downPayment', 'recurringPayment'])

# new_df['brand'] = label_encoder.fit_transform(new_df['brand'])
car_types = new_df.brand.unique()
sigment_types = new_df.segment.unique()

# Testing/debug cases
# print(sigment_types)
# print(car_types)

while True:
    try:
        print("******* Options to see total data ******* ")
        print("0 : Quit")
        print("1 : Total K Mean Cluster")
        print("2 : Total DB Scan Cluster")
        print("3 : Total Scatter Plot Based on Brands")
        user_input = input("please enter a number for plot : ")
        user_input = int(user_input)
        user_key = user_input

        X = new_df[['recurringPayment', 'downPayment']]

        if user_key == 0:
            quit()

        elif user_key == 1:
            augmented_X = X.copy()
            kmeans = KMeans(n_clusters=4)
            kmeans.fit(X)
            kmeans.predict(X)

            sc = StandardScaler()
            X_scaled = sc.fit_transform(X)

            plt.scatter(x=X['downPayment'], y=X['recurringPayment'], c=kmeans.fit_predict(X_scaled))
            plt.xlabel("Down Payment")
            plt.ylabel("Recurring Payment")
            plt.title('Total K Means Cluster Plot ')
            plt.show()

        elif user_key == 2:
            augmented_X = X.copy()

            dbscan = DBSCAN()
            dbscan.fit_predict(X)

            sc = StandardScaler()
            X_scaled = sc.fit_transform(X)

            dbscan = DBSCAN()
            plt.scatter(x=X['downPayment'], y=X['recurringPayment'], c=dbscan.fit_predict(X_scaled))
            plt.xlabel("Down Payment")
            plt.ylabel("Recurring Payment")
            plt.title('Total DB Scan Cluster Plot')
            plt.show()

        elif user_key == 3:
            labels = new_df.brand.unique()
            fg = seaborn.FacetGrid(data=new_df, hue='brand', height=7, aspect=2.5, )
            fg.map(plt.scatter, 'downPayment', 'recurringPayment').add_legend()
            fg.fig.suptitle('Total Scatter Plot Based on Brands ')
            plt.show()


        else:
            print("Number not in given range, Please enter from 0-3")
    except ValueError:
        print("Invalid entry, please enter a number in given range")
    # These are exception handler which allow to throw a statement when input is not valid.



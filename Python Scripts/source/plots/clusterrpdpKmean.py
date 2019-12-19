# This is a cluster plot based on recurring payment and down payment based on kMeans algorithm.
# Which is filtered by the segment chosen by the user
# Core Libraries
import pandas as pd
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
# Visualization Libraries
import matplotlib.pyplot as plt
# Library Settings
plt.rcParams['figure.figsize'] = (20, 7.5)
# Helps ignore any data warnings
import warnings
warnings.filterwarnings("ignore")
from common.path_to_use import *

# data File
label_encoder = preprocessing.LabelEncoder()
segment_dict = {}
# data = pd.read_csv('/Users/Jeswanth/Desktop/rpDf.csv')
data = pd.read_csv(getOEMConcatData())
new_df = data.filter(items=['brand', 'segment', 'downPayment', 'recurringPayment'])

# This helps identify all the brands and puts it into car_types
car_types = new_df.brand.unique()
sigment_types = new_df.segment.unique()
sigment_types = sigment_types.tolist()
sigment_types = ["QUIT"] + sigment_types
# This identifies all segment types
# Puts them all in a list and adds quit at front of list

while True:
    try:
        for k in range(len(sigment_types)):
            segment_dict[k] = sigment_types[k]
            print(k, ":", sigment_types[k])
        user_input = input("Please enter a number in the given range or 0 to QUIT:")
        user_input = int(user_input)
        user_key = segment_dict[user_input]
        # This for loop will output all the choices with numbers next to them to choose which you'd like to see

        if user_input > 0:
            ram_smsc = new_df[(new_df["segment"] == user_key)]
            X = ram_smsc[['recurringPayment', 'downPayment']]
            labels = ram_smsc.brand.unique()

            augmented_X = X.copy()
            kmeans = KMeans(n_clusters=getNumberofClusters())
            kmeans.fit(X)
            kmeans.predict(X)
            sc = StandardScaler()
            X_scaled = sc.fit_transform(X)
            # This is the algorithm to predict and forecast kmeans clustering based on the clusters defined.

            plt.scatter(x=X['downPayment'], y=X['recurringPayment'], c=kmeans.fit_predict(X_scaled))
            plt.xlabel("Down Payment")
            plt.ylabel("Recurring Payment")
            plt.title('K Means Cluster Plot for ' + user_key)
            plt.show()
            # This is the organization to define the parameters for the plot.
        elif user_input == 0:
            quit()
        # This allows the program to quit when the user inputs a 0.

    except ValueError:
        print("Invalid entry, please enter a number in given range")
    except KeyError:
        print("please enter a number in the given range, please try it again")
    # These are exception handlers which allow to throw a statement when input is not valid.

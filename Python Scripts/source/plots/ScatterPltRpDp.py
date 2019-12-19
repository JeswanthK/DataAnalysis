# This file is shows a scatter plot based on the axis of recurring payment and down payment
# Which is filtered by the segment chosen by the user
# Plot points are color coordinated by the brands

import matplotlib.pyplot as plt
import pandas as pd
import seaborn
import numpy as np
from common.path_to_use import *

segment_dict = {}
# df1 = pd.read_csv('/Users/Jeswanth/Desktop/rpDf.csv')
df1 = pd.read_csv(getOEMConcatData())
new_df = df1.filter(items=['brand', 'segment', 'downPayment', 'recurringPayment'])

# This helps identify all the brands and puts it into car_types
car_types = new_df.brand.unique()
sigment_types = new_df.segment.unique()
sigment_types = sigment_types.tolist()
sigment_types = ["QUIT"] + sigment_types
# This identifies all segment types
# Puts them all in a list and adds quit at front of list
# Test case for sigment_types to see if QUIT gets added at the front:
# print(sigment_types)

while True:
    try:
        for k in range(len(sigment_types)):
            segment_dict[k] = sigment_types[k]
            print(k, ":", sigment_types[k])
        user_input = int(input("please enter a number for segment or 0 to QUIT :"))
        # user_input = int(user_input)
        user_key = segment_dict[user_input]
        # This for loop will output all the choices with numbers next to them to choose which you'd like to see

        if user_input > 0:
                ram_smsc = new_df[(new_df["segment"] == user_key)]
                X = ram_smsc["downPayment"]
                Y = ram_smsc["recurringPayment"]
                labels = ram_smsc.brand.unique()
                fg = seaborn.FacetGrid(data=ram_smsc, hue='brand', height=7, aspect=2.5)
                fg.map(plt.scatter, 'downPayment', 'recurringPayment').add_legend()
                fg.fig.suptitle('Scatter Plot for ' + user_key)
                plt.show()
        elif user_input == 0:
            quit()
        # This is where you select which segment you'd like to out put or whether you'd like to quit program

    except ValueError:
        print("Invalid entry, please enter a number in given range")

    except KeyError:
        print("please enter a number in the given range, please try it again")
    # These are exception handlers which allow to throw a statement when input is not valid.

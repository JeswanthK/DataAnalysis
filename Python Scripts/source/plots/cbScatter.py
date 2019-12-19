# This file is shows a scatter plot based on cash bonus
# Which is filtered by the segment chosen by the user
# Plot points are color coordinated by the brands
# Libraries  needed
import matplotlib.pyplot as plt
import pandas as pd
import seaborn
from common.path_to_use import *

segment_dict = {}
month_dict = {}
#df1 = pd.read_csv('/Users/Jeswanth/Desktop/oem.csv')
df1 = pd.read_csv(getOEMConcatData())
new_df = df1.filter(items=['brand', 'segment', 'cashBonus', 'month','week']).dropna()

# This helps identify all the brands and puts it into car_types and month_types
car_types = new_df.brand.unique()
month_types = new_df.month.unique()
sigment_types = new_df.segment.unique()
sigment_types = sigment_types.tolist()
sigment_types = ["QUIT"] + sigment_types
# This identifies all segment types
# Puts them all in a list and adds quit at front of list

while True:
    try:
        for k in range(len(sigment_types)):
            segment_dict[k]  = sigment_types[k]
            print(k,":",sigment_types[k])
        user_input = input("please enter a number for segment or 0 to QUIT :")
        user_input = int(user_input)
        user_key = segment_dict[user_input]
        # This for loop will output all the choices with numbers next to them to choose which you'd like to see

        if user_input > 0:
            ram_smsc = new_df[(new_df["segment"]==user_key)]
            X = ram_smsc["month"]
            Y = ram_smsc["cashBonus"]
            labels = ram_smsc.brand.unique()

            fg = seaborn.FacetGrid(data=ram_smsc, hue='brand',height=7,aspect=2.5)
            fg.map(plt.scatter, 'month', 'cashBonus').add_legend()
            fg.fig.suptitle('Cluster Plot for Cash Bonus of '+user_key)
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




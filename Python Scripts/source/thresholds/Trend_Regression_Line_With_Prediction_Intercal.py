
"""
    Title:  FCA Competitive Messaging
    Class:  CSC 4996 Senior Project, Wayne State University
    Date:   November 25, 2019


"""


# Python Libraries
# -------------------------------------------------
from sklearn.linear_model import LinearRegression
import numpy as np
from matplotlib import pyplot as plt
from math import *
import sys

sys.path.append('../')


# .env file for PATH to get the data location
# -------------------------------------------------
from common.path_to_use import *


def getTrendLineWithSingleVar(x, y, xForPrediction, predIntervalPct = 95, \
                              printPlot = False, printMsg = False):
    """
    Method takes in x and y axis data in a list that will be used to determine the upper and lower
    thresholds limit. y-axis represents the data available such as cash bonus. x-axis represents the
    time series of the data from oldest to latest date.

    NOTE: For every y-axis element, there has to be exactly one x-axis in the exact position of
    the x and y list.
    Ex. x = [1, 1, 1, 2, 3, 3, 4, 5, 5]
        y = [32, 45, 28, 36, 47, 45, 23, 41, 39]

    If there are multiple y-axis for each x-axis, then list should repeat the x-axis for the number
    of y-axis with respect to y-axis data position in the list.

    Library: "sklearn.linear_model import LinearRegression" In use does not support multidimensional
    array.
        x = [1,2,3,4,5]
        y = [[32,45,28],[36],[47,45],[23],[41,39]]

    Method also takes in a second x-axis parameter that does not hold any duplicated x-axis.
    Ex. xForPrediction = [1, 2, 3, 4, 5]

    sum of error: sigma[t=1 to n]( (actual value position - regression line position)**2 )

    Standard Deviation Formula: sqrt( (1 / (n-2)) * sum of errors)

    # Formula reference: https://people.duke.edu/~rnau/mathreg.htm
    # Code reference: https://machinelearningmastery.com/prediction-intervals-for-machine-learning/

    :param x: A list of all the x-axis values with respect to y-axis.
    :param y: A list of all the y-axis values with respect to x-axis.
    :param xForPrediction: A list of x axis values without duplicates.
    :param predIntervalPct: A floating point number that represent prediction interval percentage.
    :param printPlot: A boolean, True only if the user want to print plot as data gets analyzed.
    :param printMsg: A boolean, True only if the user want to print messages within as method
    process data.
    :return: Two lists, first containing the upper limit of thresholds and second contains
    the lower limits.

    NOTE: This shows how prediction interval percentage affects the thresholds:

    Initial Data:
    x = [1, 1, 1, 2, 3, 3, 4, 5, 5]
    y = [32, 45, 28, 36, 47, 45, 23, 41, 39]
    xForPrediction = [1, 2, 3, 4, 5]

    Prediction Interval Percentage: 0
    Thresholds Upper Limit:  [45, 46, 46, 47, 47]
    Thresholds Lower Limit:  [27, 28, 29, 29, 30]

    Prediction Interval Percentage: 25
    Thresholds Upper Limit:  [47, 48, 49, 49, 50]
    Thresholds Lower Limit:  [25, 26, 26, 27, 27]

    Prediction Interval Percentage: 50
    Thresholds Upper Limit:  [50, 50, 51, 51, 52]
    Thresholds Lower Limit:  [23, 24, 24, 25, 25]

    Prediction Interval Percentage: 75
    Thresholds Upper Limit:  [52, 52, 53, 54, 54]
    Thresholds Lower Limit:  [21, 21, 22, 22, 23]

    Prediction Interval Percentage: 95
    Thresholds Upper Limit:  [54, 54, 55, 55, 56]
    Thresholds Lower Limit:  [19, 20, 20, 21, 21]

    Prediction Interval Percentage: 100
    Thresholds Upper Limit:  [54, 55, 55, 56, 56]
    Thresholds Lower Limit:  [19, 19, 20, 20, 21]

    Prediction Interval Percentage: 115
    Thresholds Upper Limit:  [55, 56, 56, 57, 58]
    Thresholds Lower Limit:  [17, 18, 18, 19, 19]
    """

    # If length of our data list is less then 2, then we cannot run the prediction interval
    # because when finding the standard deviation for prediction interval, the formula
    # says: 1 / ((length of n) - 2) and if the length is 2, then it will result in division
    # by zero.
    lenX = len(x)
    if lenX <= 2:
        yAxisPredictionUpper = [np.nan for i in range(lenX)]
        yAxisPredictionLower = [np.nan for i in range(lenX)]

        # Returns nan for both upper and lower thresholds because not enough data to
        # implement regression. (lenX <= 2 is True)
        return (yAxisPredictionUpper, yAxisPredictionLower)

    x = np.array(x).reshape(-1,1)
    y = np.array(y)

    # To get the final prediction result without duplicate x values
    xForPredict = np.array(xForPrediction).reshape(-1,1)

    linReg = LinearRegression()
    linReg.fit(x, y)

    slope = linReg.coef_
    intercept = linReg.intercept_

    # To get the y-axis prediction of linear regression without any duplicated values.
    yPredict = list(map(lambda x: x * slope + intercept, xForPredict))

    # This is wighted yPredict. For every y-axis value, it has a x-axis value. X-axis value
    # repeats based on number of y-axis value within the x-axis.
    yAxisPrediction = list(map(lambda x: x * slope + intercept, x))

    # For each element in number of y-axis, find the difference between the actual and predicted
    # linear regression value position. Then create a list based on the differences.
    lst = []
    for i in range(len(y)):
        dd = y[i] - yAxisPrediction[i]
        lst.append(dd)

    # lst is a list that holds the difference of actual value position and linear regression line
    # position, for all the elements. Now based on the formula, we have to power the difference
    # by 2
    lst2 = list(map(lambda x: x ** 2, lst))

    # Sum all the differences of actual position and predicted position into sum_errs.
    sum_errs = sum(lst2)

    # Standard deviation formula for linear regression.
    stdev = sqrt(1 / (len(y) - 2) * sum_errs)

    # calculate prediction interval
    predictionInterval = ((predIntervalPct / 100) + 1.01) * stdev

    # If print message is true, then method will print useful data such as slope, intercept.
    if printMsg == True:
        print("Slope: ", slope)
        print("Intercept: ", intercept)
        print("stdev: ", stdev)
        print("prediction Interval", predictionInterval)

    if printPlot == True:
        yPredictUpperLine = list(map(lambda x: x + predictionInterval, yPredict))
        yPredictLowerLine = list(map(lambda x: x - predictionInterval, yPredict))

        plt.scatter(x, y)
        plt.plot(xForPredict, yPredict, color='blue')
        plt.plot(xForPredict, yPredictUpperLine, color='black')
        plt.plot(xForPredict, yPredictLowerLine, color='black')

        plt.show()

    # Based on the prediction interval, create a upper and lower thresholds for the data given.
    yAxisPredictionUpper = []
    yAxisPredictionLower = []
    for key in yPredict:
        upper = int(round(key[0] + predictionInterval))
        lower = int(round(key[0] - predictionInterval))
        if lower < 0:
            lower = np.nan

        yAxisPredictionUpper.append(upper)
        yAxisPredictionLower.append(lower)

    return (yAxisPredictionUpper, yAxisPredictionLower)


# # # ***************************************************
# # # Test/Debugging Methods
# # # ***************************************************


def test_getTrendLineWithSingleVar():
    x = [1, 1, 1, 2, 3, 3, 4, 5, 5]
    y = [32, 45, 28, 36, 47, 45, 23, 41, 39]
    xForPrediction = [1, 2, 3, 4, 5]

    printPlot = getBooleanFromENV(getPrintPlot())
    printMsg = getBooleanFromENV(getPrintMsg())
    predIntervalPct = getPredIntervalPct()

    yAxisPredictionUpper, yAxisPredictionLower = \
        getTrendLineWithSingleVar(x, y, xForPrediction, predIntervalPct, printPlot, printMsg)

    print("Thresholds Upper Limit:", yAxisPredictionUpper)
    print("Thresholds Lower Limit:", yAxisPredictionLower)


# # # ***************************************************
# # # Test/Debugging Cases
# # # ***************************************************

# # Uncomment each method call that needs to be tested.
# # NOTE: Do not test more then one method at once
# --------------------------------------------------------


# # Test/Debugging: Get trend line using linear regression.
# *************************************************

# test_getTrendLineWithSingleVar()



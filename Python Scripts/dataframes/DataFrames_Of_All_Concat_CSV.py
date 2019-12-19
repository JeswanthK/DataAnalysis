
"""
    Title:  FCA Competitive Messaging
    Class:  CSC 4996 Senior Project, Wayne State University
    Date:   November 25, 2019


"""


# Python Libraries
# -------------------------------------------------
from datetime import *
import pandas as pd
import numpy as np
import sys

sys.path.append('../')


# FCA Competitive Messaging Python Files
# -------------------------------------------------
import source.thresholds.Trend_Regression_Line_With_Prediction_Intercal as trendLine


# .env file for PATH to get the data location
# -------------------------------------------------
from common.path_to_use import *


def dateIncrementer(date):
    """
    Increments day by 1, Ex. Receive 2019-07-15, return 2019-07-16

    :param date: Date Object date
    :return: Date Object date
    """

    newDate = date + timedelta(days=1)

    return newDate


def dateDecrementer(latestDate, numDaysToGoBack):
    """
    Decrement day by given number of days, Ex. Receive 2019-07-15 and 2, return 2019-07-13.
    Return is a DateTime.Date object that consists the date.

    :param latestDate: Date object date; What is the latest date of data that we have available;
            From what day do you want to decrement the date.
    :param numDaysToGoBack: Number of days to remove from the latest available dates.
    :return: Date object of date after going back number of days from the given latest date.
    """

    decrementDate = latestDate - timedelta(days=numDaysToGoBack)

    return decrementDate


def getDates(dfAll):
    """
    Method takes a Pandas data frame and creates a list of all the unique dates from
    the data frames date column. Then, it returns the oldest date, latest date and list
    of all the available dates within the data. Also, return output results in this order
    as well.

    :param dfAll: Pandas data frame.
    :return: oldest date, latest date, and list of all the dates within the data.
    """

    dataDates = dfAll['dateCaptured'].drop_duplicates().tolist()
    dataDates.sort()

    oldestDate = min(dataDates)
    latestDate = max(dataDates)

    return oldestDate, latestDate, dataDates


def getDFOfAllConcatCSV(PATH):
    """
    Method takes in a directory path of where the concatenated csv file of either the OEM
    or Endemic data is located. Then it converts the file into a Pandas data frame. Method
    also converts the date column of data, which is in string format in Pandas data frame,
    and coverts it into a date objects columns.

    :param PATH: Directory path of all concatenate csv.
    :return: Pandas data frame of directory file.
    """

    dfAll = pd.read_csv(PATH, low_memory=False)

    dfAll['dateCaptured'] = pd.to_datetime(dfAll['dateCaptured']).dt.date

    return dfAll


def getDFForSpecificNumDaysData(dfAll, decrementDate, oldestDate, colList):
    """
    Checks if the data given to us is more then what specified by the client. If thats the
    case, Program will reduce the data to the given number of days. Default setup for analysis
    is to use recent 90 days of data.

    :param dfAll: Pandas data frame that holds all the data after converting the csv file into
    the Pandas data frame.
    :param decrementDate: The date that we should start analysis with.
    :param oldestDate: What is the oldest date of data that was in the original data frame (dfAll).
    :param colList: What columns to extract from the original data for analysis.
    :return: Pandas data frame that holds data within the specified days with only the specific
    columns that is required for analysis.
    """

    colToGet = ['dateCaptured', 'segment']
    colToGet.extend(colList)

    if decrementDate > oldestDate:
        df = dfAll.loc[dfAll['dateCaptured'] >= decrementDate, colToGet]

    elif decrementDate <= oldestDate:
        df = dfAll[colToGet]

    return df


def getUniqueDF(dfAll):
    """
    Takes in data frame of all the data and returns only the unique occurrence of each row as
    a data frame. Method keeps the first occurrence of duplicate data. By keeping the first
    occurrence of data row, we can eliminate duplicate alerts to the user as some sales goes
    for months and we want to alert user only once for the specific occurrence of unusual sale.

    :param dfAll: Pandas data frame of all the data. The original data frame that was created
    from the given csv file.
    :return: Pandas data frame that consists of only the unique rows of data.
    """

    dfUnique = dfAll.drop_duplicates(subset=dfAll.columns.difference(['dateCaptured']))

    return dfUnique


def getUniqueDFForAlerts(dfUnique, alertStartDate, latestDate, dataType = "OEM"):
    """
    Takes in the unique Pandas data frame that was build from the original data frame and also
    takes in a date. Then, method returns a new data frame with only data consists of given date
    to the most recent date available.

    :param dfUnique: Pandas data frame that has only the unique data rows.
    :param alertStartDate: Date object date that you want the new data frames data to start on.
    :param latestDate: Date object of the latest date data available.
    :return: Pandas data frame with only the given data date to most recent unique data.
    """

    # Get the previous latest date. If return == None, then there is no previous latest date.
    prevLatestDate = getLatestDateOfPrevRun(latestDate, dataType)
    regularAlertsPeriod = getRegularAlertsPeriod()
    alertStartDateByPeriod = latestDate - timedelta(days=regularAlertsPeriod)

    # Give alerts for the default number of days specified in the .env file
    if prevLatestDate == None:
        dfUniqueForAlerts = dfUnique.loc[dfUnique['dateCaptured'] >= alertStartDate]

    # If previous latest date and current latest date is same or previous latest date is bigger,
    # then no need to send alerts because we have already alerted user for this.
    elif prevLatestDate >= latestDate:
        if regularAlertsPeriod != 0:
            dfUniqueForAlerts = dfUnique.loc[dfUnique['dateCaptured'] >= alertStartDateByPeriod]

        else:
            exit()

    else:
        difference = (latestDate - prevLatestDate).days

        # Alert the user for data only between after previous alerts date to current date.
        # If time period is greater then the user specified time period, then alert user for
        # data that is within the specified time period.
        if regularAlertsPeriod != 0:
            if difference <= regularAlertsPeriod:
                dfUniqueForAlerts = dfUnique.loc[dfUnique['dateCaptured'] >= prevLatestDate]
            else:
                dfUniqueForAlerts = dfUnique.loc[dfUnique['dateCaptured'] >= alertStartDateByPeriod]

        # If user wants to get alerts from previous date to current date, regardless of the specified
        # time period, Regular_Alerts_Period_Number_Of_Days = 0, in .env file.
        else:
            dfUniqueForAlerts = dfUnique.loc[dfUnique['dateCaptured'] >= prevLatestDate]

    return dfUniqueForAlerts


def getLatestDateOfPrevRun(latestDate, dataType):
    """
    Returns the previous latest date and writes the new latest date in a text file. If no date is
    available, method writes the latest date into the text file and returns None.

    :param latestDate: Date object of the latest date data available.
    :return: Date object of previous latest date or None if no previous date available.
    """

    # Get the latest date based on current working data type.
    if dataType == "OEM":
        latestDateFile = getLatestDateHolderOEM()

    elif dataType == "Endemic":
        latestDateFile = getLatestDateHolderEndemic()

    else:
        print("Parameter variable dataType:", dataType)
        print("Variable did not received an appropriate respond")
        print("File: DataFrames_Of_All_Concat_CSV.py    Line ~= 212")
        exit()

    prevLatestDate = None

    # Read from the file only if file exists.
    if os.path.exists(latestDateFile):
        with open(latestDateFile, 'r+') as file:
            prevLatestDateStr = file.readline()
            lineLength = len(prevLatestDateStr)

            file.seek(0)

            if lineLength >= 10:
                year1 = int(prevLatestDateStr[0:4])
                month1 = int(prevLatestDateStr[5:7])
                day1 = int(prevLatestDateStr[8:10])
                prevLatestDate = date(year1, month1, day1)

                file.truncate(0)
                file.write(str(latestDate))

            else:
                file.truncate(0)
                file.write(str(latestDate))

    # If file does not exist, create a file and write the given latest date.
    else:
        with open(latestDateFile, 'w+') as file:
            file.write(str(latestDate))

    return prevLatestDate


def getSegmentList(df):
    """
    Takes in the Pandas data frame that needs to be analyzed and goes through its "segment"
    column to find all the segments available within the given data.

    :param df: Pandas data frame that holds the data that needs to be analyzed.
    :return: A list of all the unique segments that is in the analysis data frame.
    """

    segList = df.segment.dropna().unique().tolist()

    return segList


def getEachSegData(df, segment):
    """
    Method takes in the data frame of all the data that needs to be analyzed and returns only
    the data that relates to given segment name as a Pandas data frame.

    :param df: Pandas data frame; data frame consists of all the data that needs to be analyzed.
    :param segment: segment name; Which segment of data need to be extracted from all the data.
    :return: Pandas data frame; Data frame consists of data for only specified segment.
    """

    isSegment = df['segment'] == segment
    dfSeg = df[isSegment]

    return dfSeg


def getCBPerSegDF(dfSegCol, oldestDate, latestDate, dataDates, segment, col, predIntervalPct, \
                  printPlot, printMsg):
    """
    Takes in the segment data that needs to analyzed along with the oldest date, latest date
    and all the dates that holds data for the analysis. It also carries parameters that will
    be used by another methods (Linear Regression) within the body of this method.

    This method takes in the required data and arranges then in a format that will be used by
    regression method to give us a weighted linear regression. Ex. If we have 5 y-axis value
    for a single x-axis value, this method will create a list containing 5 same x-axis value
    and pass it as x-axis. Ex. y-axis = [[1,2,3,4,5], [5,4,3,2,1]] and x-axis = [1,2], then it
    will make a new y axis = [1,2,3,4,5,5,4,3,2,1] and x-axis = [1,1,1,1,1,2,2,2,2,2].

    The reasoning behind this is that the regression library that we are using in this program
    does not support multidimensional array.
    Regression Library: from sklearn.linear_model import LinearRegression

    :param dfSegCol: Pandas data frame with only a specific segment data.
    :param oldestDate: Date object with the oldest date within the data frame given.
    :param latestDate: Date object with the latest date within the data frame given.
    :param dataDates: List of all the dates with data that is available in our data frame that
    being analyzed. Not the data frame given to this method but rather the data frame that was
    used to extract the data to pass to this method.
    :param segment: Segment name who's data is being analyzed.
    :param col: Column name within the given segment who's data is being analyzed.
    :param predIntervalPct: Double (Default: 95), What percentage of prediction interval should
    be used to find the upper and lower thresholds.
    :param printPlot: Boolean (Default False), Do the user want to visualize the linear
    regression plot as the data being analyzed. Recommend True only when debugging the debugging
    the software.
    :param printMsg: Boolean (Default False), Do the user want to print messages in Python IDE
    Console while the the program runs. Recommend True only when debugging the debugging the
    software.
    :return: Two lists. First list consist of all the data upper limit for thresholds and second
    list consists of all the lower limit for thresholds of all the dates given in parameter
    dataDates list.
    """

    date = oldestDate

    x = []
    y = []
    xForPrediction = []
    dataDate = []
    treshIdxList = []

    # By default, threshold holds only nan (Data not available). As  we receive data for
    # thresholds, we replace, nan with actual values.
    thresholdsListU = [np.nan for i in range(len(dataDates))]
    thresholdsListL = [np.nan for i in range(len(dataDates))]

    iVal = 1
    while date <= latestDate:

        isDate = dfSegCol['dateCaptured'] == date
        dfSegColByDate = dfSegCol[isDate]

        # If there is no data for a specific day, then continue to next day.
        if len(dfSegColByDate) <= 0:
            iVal += 1
            date = dateIncrementer(date)
            continue

        if (date in dataDates):
            index = dataDates.index(date)
            treshIdxList.append(index)

        # We are using repeated x values for multiple occurrence of y values, we don't want
        # to get regression for all the repeated x values. That's why we will use this list
        # which holds only unique x values that carries data for the regression.
        xForPrediction.append(iVal)
        dataDate.append(date)

        yTemp = dfSegColByDate[col].tolist()

        xTemp = [iVal for i in range(len(yTemp))]

        x.extend(xTemp)
        y.extend(yTemp)

        iVal += 1
        date = dateIncrementer(date)

    # The regression method that takes in the formatted data and returns an upper and lower
    # thresholds limit.
    trendLineWthPIUpper, trendLineWthPILower = \
        trendLine.getTrendLineWithSingleVar(x, y, xForPrediction, predIntervalPct, printPlot, printMsg)

    # When thresholds are returned, we replace all the nan values with actual thresholds.
    j = 0;
    for idx in treshIdxList:
        thresholdsListU[idx] = trendLineWthPIUpper[j]
        thresholdsListL[idx] = trendLineWthPILower[j]
        j += 1

    return (thresholdsListU, thresholdsListL)


# # # ***************************************************
# # # Test/Debugging Methods
# # # ***************************************************


def test_dateIncrementer():
    date1 = date(2019, 1, 1)
    date2 = dateIncrementer(date1)
    print("Date before: ", date1)
    print("Date after: ", date2)


def test_dateDecrementer():
    date1 = date(2019,1,1)
    defaultAlertsNumDays = getDefaultAlertsNumDays()
    date2 = dateDecrementer(date1, defaultAlertsNumDays)
    print("Date before: ", date1)
    print("Date after decrementing the number of days given in .env file for", end="")
    print(" the default alerts(", defaultAlertsNumDays, "): ", date2)


def test_getDates():
    PATH = getOEMConcatData()
    dfAll = getDFOfAllConcatCSV(PATH)
    oldestDate, latestDate, dataDates = getDates(dfAll)
    print("Oldest date: ", oldestDate)
    print("Latest date: ", latestDate)
    print("All dates list: \n", dataDates)


def test_getDFOfAllConcatCSV():
    PATH = getOEMConcatData()
    dfAll = getDFOfAllConcatCSV(PATH)
    print(dfAll)


def test_getDFForSpecificNumDaysData():
    PATH = getOEMConcatData()
    dfAll = getDFOfAllConcatCSV(PATH)
    oldestDate, latestDate, dataDates = getDates(dfAll)
    numDaysToGoBack = getNumDaysToGoBack()
    decrementDate = dateDecrementer(latestDate, numDaysToGoBack)
    colList = getListFromStrByComma(getThresholdsAlertsCol())

    df = getDFForSpecificNumDaysData(dfAll, decrementDate, oldestDate, colList)
    print(df)


def test_getUniqueDF():
    PATH = getOEMConcatData()
    dfAll = getDFOfAllConcatCSV(PATH)

    dfUnique = getUniqueDF(dfAll)
    print(dfUnique)


def test_getUniqueDFForAlerts():
    PATH = getOEMConcatData()
    defaultAlertsNumDays = int(getDefaultAlertsNumDays())

    dfAll = getDFOfAllConcatCSV(PATH)
    oldestDate, latestDate, dataDates = getDates(dfAll)

    dfUnique = getUniqueDF(dfAll)
    alertStartDate = dateDecrementer(latestDate, defaultAlertsNumDays)

    dataType = "OEM"

    dfUniqueForAlerts = getUniqueDFForAlerts(dfUnique, alertStartDate, latestDate, dataType)
    print(dfUniqueForAlerts)


def test_getSegmentList():
    PATH = getOEMConcatData()
    dfAll = getDFOfAllConcatCSV(PATH)

    oldestDate, latestDate, dataDates = getDates(dfAll)
    numDaysToGoBack = getNumDaysToGoBack()
    decrementDate = dateDecrementer(latestDate, numDaysToGoBack)
    colList = getListFromStrByComma(getThresholdsAlertsCol())

    df = getDFForSpecificNumDaysData(dfAll, decrementDate, oldestDate, colList)
    segList = getSegmentList(df)
    print(segList)


def test_getEachSegData():
    PATH = getOEMConcatData()
    dfAll = getDFOfAllConcatCSV(PATH)

    oldestDate, latestDate, dataDates = getDates(dfAll)
    numDaysToGoBack = getNumDaysToGoBack()
    decrementDate = dateDecrementer(latestDate, numDaysToGoBack)
    colList = getListFromStrByComma(getThresholdsAlertsCol())

    df = getDFForSpecificNumDaysData(dfAll, decrementDate, oldestDate, colList)
    segList = getSegmentList(df)

    segment = segList[0]
    dfSeg = getEachSegData(df, segment)
    print("Segment: ", segment)
    print(dfSeg)


def test_getCBPerSegDF():
    predIntervalPct = getPredIntervalPct()
    printPlot = getBooleanFromENV(getPrintPlot())
    printMsg = getBooleanFromENV(getPrintMsg())

    PATH = getOEMConcatData()
    dfAll = getDFOfAllConcatCSV(PATH)

    oldestDate, latestDate, dataDates = getDates(dfAll)
    numDaysToGoBack = getNumDaysToGoBack()
    decrementDate = dateDecrementer(latestDate, numDaysToGoBack)
    colList = getListFromStrByComma(getThresholdsAlertsCol())

    df = getDFForSpecificNumDaysData(dfAll, decrementDate, oldestDate, colList)

    # Update the dates with current working data frame.
    oldestDate, latestDate, dataDates = getDates(df)

    segList = getSegmentList(df)

    segment = segList[0]
    dfSeg = getEachSegData(df, segment)
    col = colList[0]

    dfSegCol = dfSeg[['dateCaptured', col]].dropna(subset=[col])

    thresholdsListU, thresholdsListL = \
        getCBPerSegDF(dfSegCol, oldestDate, latestDate, dataDates, segment, col,
                      predIntervalPct, printPlot, printMsg)

    print("Segment: ", segment)
    print("Column: ", col)
    print("Thresholds Upper Limit: ", thresholdsListU)
    print("Thresholds Lower Limit: ", thresholdsListL)


# # # ***************************************************
# # # Test/Debugging Cases
# # # ***************************************************

# # Uncomment each method call that needs to be tested.
# # NOTE: Do not test more then one method at once
# --------------------------------------------------------


# # Test/Debugging: Date incrementer increments date by one day.
# *************************************************

# test_dateIncrementer()


# # Test/Debugging: Date decrement by specific number of days.
# *************************************************

# test_dateDecrementer()


# # Test/Debugging: Get the oldest and latest date and a list of all the dates from the original
# # csv file data frame.
# *************************************************

# test_getDates()


# # Test/Debugging: Convert the csv file into a Pandas data frame.
# *************************************************

# test_getDFOfAllConcatCSV()


# # Test/Debugging: Get data frame for only a specific number of days. E.g. In the given CSV file,
# # if there is data of more then 90 days, then we will only take up to 90(Default) days of
# # data from the most recent date.
# *************************************************

# test_getDFForSpecificNumDaysData()


# # Test/Debugging: Get unique rows(no duplicate rows) of all the data from original Pandas data frame.
# *************************************************

# test_getUniqueDF()


# # Test/Debugging: From the unique rows data frame, get only the data that is needed for alerts.
# *************************************************

# test_getUniqueDFForAlerts()


# # Test/Debugging: Get a list of all the segments within the analysis data frame.
# *************************************************

# test_getSegmentList()


# # Test/Debugging: Get each segment's data from analysis data frame.
# *************************************************

# test_getEachSegData()


# # Test/Debugging: Get the upper and lower thresholds.
# *************************************************

# test_getCBPerSegDF()



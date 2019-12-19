
"""
    Title:  FCA Competitive Messaging
    Class:  CSC 4996 Senior Project, Wayne State University
    Date:   November 25, 2019


"""


# Python Libraries
# -------------------------------------------------
import pandas as pd
import numpy as np
from datetime import *
import sys

sys.path.append('../')


# FCA Competitive Messaging Python Files
# -------------------------------------------------
import dataframes.DataFrames_Of_All_Concat_CSV as dfAllConcat


# .env file for PATH to get the data location
# -------------------------------------------------
from common.path_to_use import *


def getUpperLowerColList(colList):
    """
    Method takes in a list of columns and returns a new column list where for every column
    element in the given list, there will be two elements in new list.
    first element: original column element + Upper
    second element: original column element + lower

    :param colList: List of columns that needs to be analyzed.
    :return: List for thresholds method to store both upper and lower limit for each column.
    """

    newColList = []
    for i in colList:
        newColList.append(i+'Upper')
        newColList.append(i+'Lower')

    return newColList


def getThresholds(df, oldestDate, latestDate, dataDates, segList, colList, \
                                               predIntervalPct, printPlot, printMsg):
    """
    Takes in the data and all the columns that needs to be analyzed and outputs a Pandas data
    frame of both upper and lower thresholds for all the specified columns. Ex.
      date    |   Segment |   cashBonusUpper
    ------------------------------------------
    2019/7/15 | Small Van |   2500
    2019/7/15 |Compact Car|   2000
    2019/7/15 | SUV       |   3850
    2019/7/16 | Small Van |   2300
    2019/7/16 |Compact Car|   1700
    2019/7/16 | SUV       |   4000

    :param df: Pandas data frame that holds all the data that is being analyzed.
    :param oldestDate: Date object with the oldest date within the data frame given.
    :param latestDate: Date object with the latest date within the data frame given.
    :param dataDates: List of all the dates with data that is available in our data frame that
    being analyzed. Not the data frame given to this method but rather the data frame that was
    used to extract the data to pass to this method.
    :param segList: List of all the segment type.
    :param colList: List of all the columns within the data frame that is being analyzed.
    :param predIntervalPct: Double (Default: 95), What percentage of prediction interval should
    be used to find the upper and lower thresholds.
    :param printPlot: Boolean (Default False), Do the user want to visualize the linear
    regression plot as the data being analyzed. Recommend True only when debugging the debugging
    the software.
    :param printMsg: Boolean (Default False), Do the user want to print messages in Python IDE
    Console while the the program runs. Recommend True only when debugging the debugging the
    software.
    :return: Pandas data frame consists of all the thresholds.
    """

    dfThresholdListU = []
    dfThresholdListL = []
    allColThresByDateList = []

    for segment in segList:
        # Data frame consists of data for only the current segment.
        dfSeg = dfAllConcat.getEachSegData(df, segment)

        allThresholdsListU = []
        allThresholdsListL = []

        if len(dfSeg) <= 0:
            # Assign a NULL/nan value to all the thresholds whom belong to a segment that does
            # not contain any data within the working data frame for the specific segment.
            allThresholdsListU = [[np.nan for i in range(len(colList))] for i in range(len(dataDates))]
            dfThresholdListU.append(allThresholdsListU)

            allThresholdsListL = [[np.nan for i in range(len(colList))] for i in range(len(dataDates))]
            dfThresholdListL.append(allThresholdsListL)

            continue

        # Within each segment, get the thresholds for all the columns specified in column list.
        for col in colList:
            dfSegCol = dfSeg[['dateCaptured', col]].dropna(subset=[col])

            thresholdsListU, thresholdsListL = \
                getEachColThresholds(dfSegCol, oldestDate, latestDate, dataDates, segment, col, \
                                               predIntervalPct, printPlot, printMsg)

            # Append upper and lower thresholds for each column into a list for current segment.
            allThresholdsListU.append(thresholdsListU)
            allThresholdsListL.append(thresholdsListL)

        # Append all columns thresholds for each segment into a list.
        dfThresholdListU.append(allThresholdsListU)
        dfThresholdListL.append(allThresholdsListL)

    # At this point, we have all the thresholds, however we need to rearrange the thresholds
    # based on given data format. E.g. date column consists of all the dates, cashBonusUpper
    # column column consists of all the thresholds for cash bonus upper limit with respect to
    # dates.
    # Ex. data frame after completing the below nested loop/scripts.

    #   date    |   Segment |   cashBonusUpper
    # ------------------------------------------
    # 2019/7/15 | Small Van |   2500
    # 2019/7/15 |Compact Car|   2000
    # 2019/7/15 | SUV       |   3850
    # 2019/7/16 | Small Van |   2300
    # 2019/7/16 |Compact Car|   1700
    # 2019/7/16 | SUV       |   4000

    # Another reason for arranging thresholds in this format is because it makes easier for
    # data visualization team to take my data into Tableau and output the visualization without
    # making major changes to their existing code since formatting of the thresholds data is
    # same as the original data that was given.

    # Currently thresholds are in multiple-nested lists.
    # [[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]],
    #  [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]]

    # []: The very first list consists of all the segments.
    # [[],[]]: Second nested list consists of all the columns within each segment.
    # [[[],[]], [[],[]]]: Third nested list consists of each columns threshold limits in the
    #                   order of oldest to latest date.

    for j in range(len(dfThresholdListU[0])):
        colThresByDateU = []
        colThresByDateL = []

        for k in range(len(dfThresholdListU[0][0])):
            for i in range(len(dfThresholdListU)):
                colThresByDateU.append(dfThresholdListU[i][j][k])
                colThresByDateL.append((dfThresholdListL[i][j][k]))

        allColThresByDateList.append(colThresByDateU)
        allColThresByDateList.append(colThresByDateL)

    # After Rearranging, the data looks like this:
    # [[1, 1, 2, 2, 3, 3, 4, 4],
    #  [5, 5, 6, 6, 7, 7, 8, 8],
    #  [9, 9, 10, 10, 11, 11, 12, 12],
    #  [13, 13, 14, 14, 15, 15, 16, 16]]

    # Now we have rearranged the data in a format where for each column thresholds we hve
    # segment 1 and segment 2 data.
    # Ex. data frame after completing the below nested loop/scripts.

    #   date    |   Segment | cashBonusUpper |cashBonusLower | downPaymentUpper
    # ------------------------------------------------------------------------------
    # 2019/7/15 | Small Van |    1           |       5       |      9
    # 2019/7/15 | SUV       |    1           |       5       |      9
    # 2019/7/16 | Small Van |    2           |       6       |      10
    # 2019/7/16 | SUV       |    2           |       6       |      10
    # 2019/7/17 | Small Van |    3           |       7       |      11
    # 2019/7/17 | SUV       |    3           |       7       |      11
    # 2019/7/18 | Small Van |    4           |       7       |      12
    # 2019/7/18 | SUV       |    4           |       7       |      12

    newColList = getUpperLowerColList(colList)

    dfOnlyThresholds = pd.DataFrame(allColThresByDateList, index=newColList).T

    initDF = getThresholdsInitDF(dataDates, segList)

    dfAllThresholds = pd.concat([initDF, dfOnlyThresholds], axis=1)

    return dfAllThresholds


def getEachColThresholds(dfSegCol, oldestDate, latestDate, dataDates, segment, col, \
                                               predIntervalPct, printPlot, printMsg):
    """
    Takes in a Pandas data frame that consist of only a specific segment and column data.
    Then, the method process the data and outputs the thresholds in lists.

    :param dfSegCol: Pandas data frame consists of all the data that belongs to current working
    segment of current column.
    :param oldestDate: Date object with the oldest date within the data frame given.
    :param latestDate: Date object with the latest date within the data frame given.
    :param dataDates: List of all the dates with data that is available in our data frame that
    being analyzed. Not the data frame given to this method but rather the data frame that was
    used to extract the data to pass to this method.
    :param segment: String, segment name for the data that is being processed.
    :param col: String, column name for the data within the segment that is being processed.
    :param predIntervalPct: Double (Default: 95), What percentage of prediction interval should
    be used to find the upper and lower thresholds.
    :param printPlot: Boolean (Default False), Do the user want to visualize the linear
    regression plot as the data being analyzed. Recommend True only when debugging the debugging
    the software.
    :param printMsg: Boolean (Default False), Do the user want to print messages in Python IDE
    Console while the the program runs. Recommend True only when debugging the debugging the
    software.
    :return: Two lists, The upper and lower limit thresholds for the current segment and column.
    """

    if len(dfSegCol) <= 0:
        thresholdsListU = [np.nan for i in range(len(dataDates))]
        thresholdsListL = [np.nan for i in range(len(dataDates))]

        return thresholdsListU, thresholdsListL

    thresholdsListU, thresholdsListL = \
        dfAllConcat.getCBPerSegDF(dfSegCol, oldestDate, latestDate, dataDates, segment, col, \
                                               predIntervalPct, printPlot, printMsg)

    return thresholdsListU, thresholdsListL


def getThresholdsInitDF(dataDates, segList):
    """
    Creates an initial data frame that consists of date and segment column completed for
    the thresholds.

    :param dataDates: List of all the dates that we are getting the thresholds for.
    :param segList: List of all the segments that is in the analysis data.
    :return: Pandas data frame with columns date and segment.
    """

    allDateList = []
    allSegList = []

    for i in range(len(dataDates)):
        dateToUse = dataDates[i]
        date = [dateToUse for i in range(len(segList))]

        allDateList.extend(date)
        allSegList.extend(segList)

    dfAllInitData = pd.DataFrame(list(zip(allDateList, allSegList)), \
                                columns=['date', 'segment'])

    return dfAllInitData


def getAllOEMThresholds(dfAllThresholds):
    """
    Takes in Pandas data frame of all the OEM thresholds and saves it into an excel file in
    the local directory.
    File Path is specified in .env file: Save_To_Thresholds_OEM

    :param dfAllThresholds: Pandas data frame of all the thresholds for OEM.
    :return: None.
    """

    dfAllThresholds.to_excel(getSaveToThresholdsOEM(), index=False)


def getAllOEMAlerts(dfAllThresholdsAlerts):
    """
    Takes in Pandas data frame of all the OEM alerts and saves it into an excel file in
    the local directory.
    File Path is specified in .env file: Save_To_Alerts_OEM

    :param dfAllThresholdsAlerts: Pandas data frame of all the alerts for OEM.
    :return: None.
    """

    dfAllThresholdsAlerts.to_excel(getSaveToAlertsOEM(), index=False)


def getAllEndemicThresholds(dfAllThresholds):
    """
    Takes in Pandas data frame of all the Endemic thresholds and saves it into an excel file in
    the local directory.
    File Path is specified in .env file: Save_To_Thresholds_Endemic

    :param dfAllThresholds: Pandas data frame of all the thresholds for Endemic.
    :return: None.
    """

    dfAllThresholds.to_excel(getSaveToThresholdsEndemic(), index=False)


def getAllEndemicAlerts(dfAllThresholdsAlerts):
    """
     Takes in Pandas data frame of all the Endemic alerts and saves it into an excel file in
    the local directory.
    File Path is specified in .env file: Save_To_Alerts_Endemic

    :param dfAllThresholdsAlerts: Pandas data frame of all the alerts for Endemic.
    :return: None.
    """

    dfAllThresholdsAlerts.to_excel(getSaveToAlertsEndemic(), index=False)


# # # ***************************************************
# # # Test/Debugging Methods
# # # ***************************************************


def test_getUpperLowerColList():
    colList = getListFromStrByComma(getThresholdsAlertsCol())
    newColList = getUpperLowerColList(colList)

    print("Column list: ", colList)
    print("New column list: ", newColList)


def test_getThresholds():
    predIntervalPct = getPredIntervalPct()
    printPlot = getBooleanFromENV(getPrintPlot())
    printMsg = getBooleanFromENV(getPrintMsg())
    numDaysToGoBack = getNumDaysToGoBack()
    colList = getListFromStrByComma(getThresholdsAlertsCol())
    PATH = getOEMConcatData()

    dfAll = dfAllConcat.getDFOfAllConcatCSV(PATH)

    oldestDate, latestDate, dataDates = dfAllConcat.getDates(dfAll)
    decrementDate = dfAllConcat.dateDecrementer(latestDate, numDaysToGoBack)

    df = dfAllConcat.getDFForSpecificNumDaysData(dfAll, decrementDate, oldestDate, colList)

    # Update the dates with current working data frame.
    oldestDate, latestDate, dataDates = dfAllConcat.getDates(df)

    segList = dfAllConcat.getSegmentList(df)

    dfAllThresholds = getThresholds(df, oldestDate, latestDate, dataDates, segList, colList, \
                  predIntervalPct, printPlot, printMsg)

    print("Data frame of all the thresholds: ")
    print(dfAllThresholds)


def test_getEachColThresholds():
    predIntervalPct = getPredIntervalPct()
    printPlot = getBooleanFromENV(getPrintPlot())
    printMsg = getBooleanFromENV(getPrintMsg())
    numDaysToGoBack = getNumDaysToGoBack()
    colList = getListFromStrByComma(getThresholdsAlertsCol())
    PATH = getOEMConcatData()

    dfAll = dfAllConcat.getDFOfAllConcatCSV(PATH)

    oldestDate, latestDate, dataDates = dfAllConcat.getDates(dfAll)
    decrementDate = dfAllConcat.dateDecrementer(latestDate, numDaysToGoBack)

    df = dfAllConcat.getDFForSpecificNumDaysData(dfAll, decrementDate, oldestDate, colList)

    # Update the dates with current working data frame.
    oldestDate, latestDate, dataDates = dfAllConcat.getDates(df)

    segList = dfAllConcat.getSegmentList(df)

    segment = segList[0]
    dfSeg = dfAllConcat.getEachSegData(df, segment)
    col = colList[0]

    dfSegCol = dfSeg[['dateCaptured', col]].dropna(subset=[col])

    thresholdsListU, thresholdsListL = \
        getEachColThresholds(dfSegCol, oldestDate, latestDate, dataDates, segment, col, \
                                               predIntervalPct, printPlot, printMsg)

    print("Thresholds upper for ", segment, col)
    print(thresholdsListU)
    print("Thresholds lower for ", segment, col)
    print(thresholdsListL)


def test_getThresholdsInitDF():
    numDaysToGoBack = getNumDaysToGoBack()
    colList = getListFromStrByComma(getThresholdsAlertsCol())
    PATH = getOEMConcatData()

    dfAll = dfAllConcat.getDFOfAllConcatCSV(PATH)

    oldestDate, latestDate, dataDates = dfAllConcat.getDates(dfAll)
    decrementDate = dfAllConcat.dateDecrementer(latestDate, numDaysToGoBack)

    df = dfAllConcat.getDFForSpecificNumDaysData(dfAll, decrementDate, oldestDate, colList)

    # Update the dates with current working data frame.
    oldestDate, latestDate, dataDates = dfAllConcat.getDates(df)

    segList = dfAllConcat.getSegmentList(df)

    dfAllInitData = getThresholdsInitDF(dataDates, segList)

    print("Initial data frame for thresholds")
    print(dfAllInitData)


# # # ***************************************************
# # # Test/Debugging Cases
# # # ***************************************************

# # Uncomment each method call that needs to be tested.
# # NOTE: Do not test more then one method at once
# --------------------------------------------------------


# # Test/Debugging: Get a new column list from the given given column in .env file where for each
# # column list element, the new list will have two column elements. Two two column elements
# # will be original column name + Upper and original column name + lower.
# *************************************************

# test_getUpperLowerColList()


# # Test/Debugging: Get a Pandas data frame of all the thresholds.
# *************************************************

# test_getThresholds()


# # Test/Debugging: Get thresholds for a specific segment and specific column.
# *************************************************

# test_getEachColThresholds()


# # Test/Debugging: Get the initial data frame for thresholds.
# *************************************************

# test_getThresholdsInitDF()






"""
    Title:  FCA Competitive Messaging
    Class:  CSC 4996 Senior Project, Wayne State University
    Date:   November 25, 2019


"""


# Python Libraries
# -------------------------------------------------
import sys

sys.path.append('../')


# FCA Competitive Messaging Python Files
# -------------------------------------------------
import pandas as pd
import dataframes.DataFrames_Of_All_Concat_CSV as dfAllConcat
import source.thresholds.Thresholds_V2 as allThresholds


# .env file for PATH to get the data location
# -------------------------------------------------
from common.path_to_use import *


def getAlerts(dfAllThresholds, dfUniqueForAlerts, colList, newColList):
    """
    Takes in a data frame that consists of all the thresholds and a second data frame of all
    the data that needs to be checked for alerts. Then, the method compares each data row of
    the second data frame to its appropriate threshold. When one or more thresholds has been
    triggered, then the method append that row of data into an alerts data frame which gets
    returned after method run.

    :param dfAllThresholds: Pandas data frame with all the thresholds
    :param dfUniqueForAlerts: Pandas data frame with data that needs to be checked for rows
    that is over its appropriate threshold limit.
    :param colList: List of all the columns that is being analyzed.
    :param newColList: List where for every column element in the colList parameter, there
    will be two elements in new list.
    first element: original column element + Upper
    second element: original column element + lower
    :return: Pandas data frame of all the rows that is over the thresholds for one or more
    specified thresholds columns.
    """

    allRowDFList = []
    allThresholdsColList = []
    allThresholdsDFList = []

    for rowIndex, row in dfUniqueForAlerts.iterrows():
        rowSegment = row['segment']
        rowDate = row['dateCaptured']

        # If the current row that is being accessed does not have segment data, then continue
        # to next row.
        if pd.isnull(rowSegment):
            continue

        # Get the appropriate thresholds based on current row's date and segment.
        dfRowThresholds = dfAllThresholds.loc[(dfAllThresholds['date'] == rowDate) & \
                                        (dfAllThresholds['segment'] == rowSegment), newColList] \
                                        .reset_index(drop=True)

        # If a column crosses threshold, that column name will be appended to this list.
        thresholdColumns = []
        doAlert = False

        # Check through all the columns to make sure non of the column crosses thresholds.
        for colIdx, col in enumerate(colList):
            upperColName = newColList[colIdx * 2]
            lowerColName = newColList[(colIdx * 2) + 1]

            # If a column data of current row is null, continue to next column of the row.
            if pd.isnull(row[col]):
                continue

            upper = float(dfRowThresholds[upperColName])
            lower = float(dfRowThresholds[lowerColName])

            if pd.isnull(upper) == False:
                if row[col] >= upper:
                    doAlert = True
                    thresholdColumns.append(upperColName)
                    continue

            elif pd.isnull(lower) == False:
                if row[col] <= lower:
                    doAlert = True
                    thresholdColumns.append(lowerColName)
                    continue

        # If any column of the current row crosses threshold, then the row will be appended
        # into a list along with the columns that caused the alerts and all the thresholds
        # that belong to that row for alerts.
        if doAlert == True:
            # Row data append
            row = row.to_frame().T.reset_index(drop=True)
            allRowDFList.append(row)

            # Column that caused alerts append
            allThresholdsColList.append(thresholdColumns)

            # All the thresholds for the current row append
            allThresholdsDFList.append(dfRowThresholds)

    # Concatenate the list of all the rows into one data frame.
    dfAllRowData = pd.concat(allRowDFList, ignore_index=True)

    # Concatenate the list of all the thresholds columns into one data frame.
    dfAllThresholdsCol = pd.DataFrame(data={'thresholdsColumns': allThresholdsColList})

    # Concatenate the list of all the thresholds rows into one data frame.
    dfAllThresholds = pd.concat(allThresholdsDFList, ignore_index=True)

    # Concatenate all 3 previous data frames into one.
    frame = [dfAllRowData, dfAllThresholdsCol, dfAllThresholds]
    dfAllThresholdsAlerts = pd.concat(frame, axis=1)

    return dfAllThresholdsAlerts


# # # ***************************************************
# # # Test/Debugging Methods
# # # ***************************************************

def test_getAlerts():
    predIntervalPct = getPredIntervalPct()
    printPlot = getBooleanFromENV(getPrintPlot())
    printMsg = getBooleanFromENV(getPrintMsg())
    numDaysToGoBack = getNumDaysToGoBack()
    defaultAlertsNumDays = getDefaultAlertsNumDays()
    colList = getListFromStrByComma(getThresholdsAlertsCol())
    PATH = getOEMConcatData()

    newColList = allThresholds.getUpperLowerColList(colList)

    dfAll = dfAllConcat.getDFOfAllConcatCSV(PATH)

    oldestDate, latestDate, dataDates = dfAllConcat.getDates(dfAll)
    decrementDate = dfAllConcat.dateDecrementer(latestDate, numDaysToGoBack)

    df = dfAllConcat.getDFForSpecificNumDaysData(dfAll, decrementDate, oldestDate, colList)

    # Update the dates with current working data frame.
    oldestDate, latestDate, dataDates = dfAllConcat.getDates(df)

    segList = dfAllConcat.getSegmentList(df)

    dfAllThresholds = allThresholds.getThresholds(df, oldestDate, latestDate, dataDates, \
                                        segList, colList, predIntervalPct, printPlot, printMsg)

    dfUnique = dfAllConcat.getUniqueDF(dfAll)
    alertStartDate = dfAllConcat.dateDecrementer(latestDate, defaultAlertsNumDays)

    dataType = "OEM"

    dfUniqueForAlerts = dfAllConcat.getUniqueDFForAlerts(dfUnique, alertStartDate, latestDate, dataType)

    dfAllThresholdsAlerts = getAlerts(dfAllThresholds, dfUniqueForAlerts, colList, newColList)

    print("Data frame of all the alerts: ")
    print(dfAllThresholdsAlerts)


# # # ***************************************************
# # # Test/Debugging Cases
# # # ***************************************************

# # Uncomment each method call that needs to be tested.
# # NOTE: Do not test more then one method at once
# --------------------------------------------------------


# # Test/Debugging: Get all the alerts for thresholds
# *************************************************

# test_getAlerts()




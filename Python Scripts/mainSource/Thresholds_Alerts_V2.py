
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
import dataframes.DataFrames_Of_All_Concat_CSV as dfAllConcat
import source.thresholds.Thresholds_V2 as allThresholds
import source.alerts.Alerts_V2 as alerts
import source.alerts.send_email as sendEmail


# .env file for PATH to get the data location
# -------------------------------------------------
from common.path_to_use import *


# Initial data from .env file.
printPlot = getBooleanFromENV(getPrintPlot())
printMsg = getBooleanFromENV(getPrintMsg())
predIntervalPct = getPredIntervalPct()
numDaysToGoBack = getNumDaysToGoBack()
defaultAlertsNumDays = getDefaultAlertsNumDays()
colList = getListFromStrByComma(getThresholdsAlertsCol())

newColList = allThresholds.getUpperLowerColList(colList)


def getOEMDataAnalysis():
    """
    The main OEM data method. Method gather all the required data needed to get analysis of OEM
    data and output thresholds and alerts into the given file names and directory in .env file.

    :return: None
    """

    PATH = str(getOEMConcatData())

    # Convert data file into Pandas data frame.
    dfAll = dfAllConcat.getDFOfAllConcatCSV(PATH)

    # Get all the appropriate dates.
    oldestDate, latestDate, dataDates = dfAllConcat.getDates(dfAll)
    decrementDate = dfAllConcat.dateDecrementer(latestDate, numDaysToGoBack)

    # New data frame consist of 90 days of data and only the columns that need to be analyzed.
    df = dfAllConcat.getDFForSpecificNumDaysData(dfAll, decrementDate, oldestDate, colList)

    # Update the dates with current working data frame.
    oldestDate, latestDate, dataDates = dfAllConcat.getDates(df)

    # Segment list from new data frame. I.g. df
    segList = dfAllConcat.getSegmentList(df)

    # Get thresholds from the analysis.
    dfAllThresholds = allThresholds.getThresholds(df, oldestDate, latestDate, dataDates, segList, \
                                                  colList, predIntervalPct, printPlot, printMsg)

    # Get the unique data frame from the original data frame which consists of only the first
    # occurrence of duplicate data row.
    dfUnique = dfAllConcat.getUniqueDF(dfAll)
    alertStartDate = dfAllConcat.dateDecrementer(latestDate, defaultAlertsNumDays)

    dataType = "OEM"

    # Get only given number of days data from unique data frame to check for alerts.
    dfUniqueForAlerts = dfAllConcat.getUniqueDFForAlerts(dfUnique, alertStartDate, latestDate, dataType)

    # New data frame consists of all the data row from unique data frame for alerts that is over one
    # or more thresholds.
    dfAllThresholdsAlerts = alerts.getAlerts(dfAllThresholds, dfUniqueForAlerts, colList, newColList)

    # Save thresholds and alerts into an excel file.
    allThresholds.getAllOEMThresholds(dfAllThresholds)
    allThresholds.getAllOEMAlerts(dfAllThresholdsAlerts)

    sendEmail.send_email(dfAllThresholdsAlerts, dataType)


def getEndemicDataAnalysis():
    """
    The main Endemic data method. Method gather all the required data needed to get analysis of
    Endemic data and output thresholds and alerts into the given file names and directory in
    .env file.

    :return: None
    """

    # Endemic data path
    PATH = str(getEndemicConcatData())

    # Convert data file into Pandas data frame.
    dfAll = dfAllConcat.getDFOfAllConcatCSV(PATH)

    # Get all the appropriate dates.
    oldestDate, latestDate, dataDates = dfAllConcat.getDates(dfAll)
    decrementDate = dfAllConcat.dateDecrementer(latestDate, numDaysToGoBack)

    # New data frame consist of 90 days of data and only the columns that need to be analyzed.
    df = dfAllConcat.getDFForSpecificNumDaysData(dfAll, decrementDate, oldestDate, colList)

    # Update the dates with current working data frame.
    oldestDate, latestDate, dataDates = dfAllConcat.getDates(df)

    # Segment list from new data frame. I.g. df
    segList = dfAllConcat.getSegmentList(df)

    # Get thresholds from the analysis.
    dfAllThresholds = allThresholds.getThresholds(df, oldestDate, latestDate, dataDates, segList, \
                                                  colList, predIntervalPct, printPlot, printMsg)

    # Get the unique data frame from the original data frame which consists of only the first
    # occurrence of duplicate data row.
    dfUnique = dfAllConcat.getUniqueDF(dfAll)
    alertStartDate = dfAllConcat.dateDecrementer(latestDate, defaultAlertsNumDays)

    dataType = "Endemic"

    # Get only given number of days data from unique data frame to check for alerts.
    dfUniqueForAlerts = dfAllConcat.getUniqueDFForAlerts(dfUnique, alertStartDate, latestDate, dataType)

    # New data frame consists of all the data row from unique data frame for alerts that is over one
    # or more thresholds.
    dfAllThresholdsAlerts = alerts.getAlerts(dfAllThresholds, dfUniqueForAlerts, colList, newColList)

    # Save thresholds and alerts into an excel file.
    allThresholds.getAllEndemicThresholds(dfAllThresholds)
    allThresholds.getAllEndemicAlerts(dfAllThresholdsAlerts)

    sendEmail.send_email(dfAllThresholdsAlerts, dataType)


def main():
    getOEMDataAnalysis()
    getEndemicDataAnalysis()


# main()


"""
    Title:  FCA Competitive Messaging
    Class:  CSC 4996 Senior Project, Wayne State University
    Date:   November 25, 2019


"""

# Python Libraries
# -------------------------------------------------
import os
from dotenv import load_dotenv
import sys

sys.path.append('../')

# Loads the .env file data into current file.
load_dotenv()


# # Get initial data and user choices.
# # ***************************************************


def getPrintPlot():
    """
    Get user choice in boolean for printing messages in Python IDE Console.

    :return: String representation of boolean choice given in .env file.
    """
    return os.getenv('Print_Plot')


def getPrintMsg():
    """
    Get user choice in boolean for printing Plot of linear regression in Python IDE Console.

    :return: String representation of boolean choice given in .env file.
    """
    return os.getenv('Print_Message')


def getPredIntervalPct():
    """
    Get the percentage of prediction interval.

    :return: float representation of prediction interval.
    """
    return float(os.getenv('Prediction_Interval_Percentage'))


def getNumDaysToGoBack():
    """
    Get the percentage of prediction interval.

    :return: Int representation of number of days to go back.
    """
    return int(os.getenv('Number_Of_Days_To_Go_Back'))


def getDefaultAlertsNumDays():
    """
    Get default alerts days. If the method is running for the first time, it will use default alerts
    days to run alerts.

    :return: Int representation of number of days to alert the user.
    """
    return int(os.getenv('Default_Alerts_Number_Of_Days'))


def getRegularAlertsPeriod():
    """
    Returns regular alert periods from .env file.

    :return: Int representation of number of days a usual alerts should be for.
    """
    return int(os.getenv('Regular_Alerts_Period_In_Number_Of_Days'))


def getThresholdsAlertsCol():
    """
    Get all the columns that needs to be analyzed.

    :return: String containing all the columns separated by comma.
    """
    return os.getenv('Thresholds_&_Alerts_Columns')


def getFCADir():
    return os.getenv('FCA_Competitive_Messaging_Dir')


def getLatestDateHolderOEM():
    """
    Returns a text file that holds the latest date of previous run for OEM.

    :return: String of text file path that holds latest date.
    """

    return getFCADir() + os.getenv('Get_Latest_Date_Holder_OEM_File')


def getLatestDateHolderEndemic():
    """
    Returns a text file that holds the latest date of previous run for Endemic.

    :return: String of text file path that holds latest date.
    """

    return getFCADir() + os.getenv('Get_Latest_Date_Holder_Endemic_File')


def getPreviousDirectoryModifiedTime():
    """
     Returns a text file that holds the latest date when the file was last modified.

    :return: String of text file path that holds latest date directory was modified.
    """
    return getFCADir() + os.getenv('Get_Previous_Directory_Modified_Time_File')


def getNumberofClusters():
    """
    Returns the number of clusters needed to be used for the clustering algorithm

    :return: integer of the number of clusters to be used
    """
    return getFCADir() + os.getenv('Number_of_Clusters')


# # Get data files and directories
# # ***************************************************


def getSegmentTypeDataPath():
    """
    Get the file path of where segment data file is located.

    :return: csv/xlsx file path that contain segment data.
    """
    return getFCADir() + os.getenv('Get_Segment_Type_Data_Path')


def getOEMDataPath():
    """
    Get the file directory of where all the OEM data is located.

    :return: File directory that contains all the OEM data files.
    """
    return getFCADir() + os.getenv('Get_All_OEM_Data_Path')


def getDataDirectoryForAnalysis():
    """
    Returns the directory that holds the data for analysis. This directory path will be used to if
    new data has been added/modified. If, then the function will run.

    :return: String file path of the analysis data.
    """
    return getFCADir() + os.getenv('Get_Data_Directory_For_Analysis')


def getEndemicDataPath():
    """
    Get the file directory of where all the Endemic data is located.

    :return: File directory that contains all the Endemic data files.
    """
    return getFCADir() + os.getenv('Get_All_Endemic_Data_Path')


def getOEMConcatData():
    """
    Get the file path where concatenated OEM data is located. A single csv file that contains all
    OEM data.

    :return: csv file path of all OEM data.
    """
    return getFCADir() + os.getenv('Get_OEM_Concat_Data')
    # return 'C:\\Users\\MRaih\\Desktop\\other_files_csv\\all_OEM_concat_test2.csv'


def getEndemicConcatData():
    """
    Get the file path where concatenated Endemic data is located. A single csv file that contains
    all Endemic data.

    :return: csv file path of all Endemic data.
    """
    return getFCADir() + os.getenv('Get_Endemic_Concat_Data')


# # Get directory and file names of where to save the data.
# # ***************************************************


def getSaveToOEMConcatPath():
    """
    Get the file path of where to save the concatenated OEM data.

    :return: file path.
    """
    return getFCADir() + os.getenv('Save_To_OEM_Concat_Data')


def getSaveToEndemicConcatPath():
    """
    Get the file path of where to save the concatenated Endemic data.

    :return: file path.
    """
    return getFCADir() + os.getenv('Save_To_Endemic_Concat_Data')


def getSaveToThresholdsOEM():
    """
    Get the file path of where to save the Thresholds OEM data.

    :return: file path.
    """
    return getFCADir() + os.getenv('Save_To_Thresholds_OEM')


def getSaveToAlertsOEM():
    """
    Get the file path of where to save the alerts OEM data.

    :return: file path.
    """
    return getFCADir() + os.getenv('Save_To_Alerts_OEM')


def getSaveToThresholdsEndemic():
    """
    Get the file path of where to save the Thresholds Endemic data.

    :return: file path.
    """
    return getFCADir() + os.getenv('Save_To_Thresholds_Endemic')


def getSaveToAlertsEndemic():
    """
    Get the file path of where to save the alerts Endemic data.

    :return: file path.
    """
    return getFCADir() + os.getenv('Save_To_Alerts_Endemic')


# # Get email info.
# # ***************************************************


def getEmail():
    """
    Get the email address that will be used to send alerts data to users.

    :return: String representation of email address.
    """
    return os.getenv('Email_Login')


def getEmailPassword():
    """
    Get the password for the given email in getEmail().

    :return: String representation of email password.
    """
    return os.getenv('Email_Password')


def getRegionalEmailLists():
    """
    Returns the csv file path that holds the data for emails. Data includes: user name, email,
    business center.

    :return: String file path of csv file that holds alerts pushing data.
    """
    return getFCADir() + os.getenv('Regional_Email_Lists')


# # Helper methods that converts boolean string to boolean and creates list based on column given
# # for analysis
# # ***************************************************


def getBooleanFromENV(var):
    """
    Takes in a string representation of a boolean variable and returns actual boolean of the
    given string. Default False.

    :param var: String boolean (True/False)
    :return: Boolean. Default False.
    """

    var = var.lower()

    if var == 'true':
        return True
    elif var == 'false':
        return False
    else:
        return False


def getListFromStrByComma(strn):
    """
    Takes in a string of column names separated by commas and returns a list of given column names.

    :param strn: String column names separated by commas.
    :return: List of column names given.
    """

    lyst = strn.split(",")

    # This list comprehension will remove any empty spaces after the split by comma.
    newList = [x.strip() for x in lyst]

    return newList

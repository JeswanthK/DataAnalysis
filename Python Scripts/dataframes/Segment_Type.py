
"""
    Title:  FCA Competitive Messaging
    Class:  CSC 4996 Senior Project, Wayne State University
    Date:   November 25, 2019


"""


# Python Libraries
# -------------------------------------------------
import os
import pandas as pd
import sys

sys.path.append('../')


# .env file for PATH to get the data location
# -------------------------------------------------
from common.path_to_use import *


def getSegmentType(PATH):
    """
    Method takes in a file path of either csv or excel, convert the data file into a pandas
    data frame and imports all the segments from Segment Type column. Then it drops the
    duplicates and returns a list of all unique segments.

    :param PATH: Directory where the segment file is located.
    :return: List of all the segments.
    """

    if os.path.exists(PATH):
        pass
    else:
        print(PATH, " is not accessible. \nPlease check the directory path.")
        print("dataframes.Segment_Type.py   Line ~= 35")
        exit()


    # To check if the given file is a CSV or Excel file.
    csv = ".csv"
    xlsx = ".xlsx"

    # Open excel/csv file into Pandas Data frame and only read specified columns
    if csv in PATH:
        segmentDataFrame = pd.read_csv(PATH)['Segment Type']
    elif xlsx in PATH:
        segmentDataFrame = pd.read_excel(PATH)['Segment Type']
    else:
        print(PATH)
        print("Segment file type is not supported. File format should either be ", end="")
        print("CSV(.csv) or Excel(.xlsx)")
        print("dataframes.Segment_Type.py   Line ~= 45")
        exit()


    # Drop duplicates to get only the unique segments
    segmentDataFrame = segmentDataFrame.drop_duplicates()

    listOfSegmentType = list(segmentDataFrame)

    return listOfSegmentType


# # # ***************************************************
# # # Test/Debugging Methods
# # # ***************************************************


def test_getSegmentType():
    PATH = getSegmentTypeDataPath()
    SegList = getSegmentType(PATH)
    print(SegList)


# # # ***************************************************
# # # Test/Debugging Cases
# # # ***************************************************

# # Uncomment each method call that needs to be tested.
# # NOTE: Do not test more then one method at once
# --------------------------------------------------------


# # Test getSegmentType(PATH) (Get Segment Type)
# *************************************************

# test_getSegmentType()









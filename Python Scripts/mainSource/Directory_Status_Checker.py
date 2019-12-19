
"""
    Title:  FCA Competitive Messaging
    Class:  CSC 4996 Senior Project, Wayne State University
    Date:   December 03, 2019


"""


# Python Libraries
# -------------------------------------------------
import os
import time
import sys

sys.path.append('../')


# FCA Competitive Messaging Python Files
# -------------------------------------------------


# .env file for PATH to get the data location
# -------------------------------------------------
from common.path_to_use import *


def getLastModifiedTime(PATH):

    try:
        lastModifiedTime = time.ctime(os.path.getmtime(PATH))
        # lastModifiedTime = time.ctime(max(os.path.getmtime(root) for root, _, _ in os.walk(PATH)))

    except OSError:
        print(PATH)
        print("Given PATH does not exist or inaccessible")
        print("Directory_Status_Checker.py  Line ~= 25")
        exit()

    return lastModifiedTime


def getIsPrevModifiedDateChanged():

    PATH1 = getDataDirectoryForAnalysis()
    CurrentModifiedTime = getLastModifiedTime(PATH1)

    PATH = getPreviousDirectoryModifiedTime()

    booleanRunProgram = True

    # Read from the file only if file exists.
    if os.path.exists(PATH):
        with open(PATH, 'r+') as file:
            prevModifiedDateStr = file.readline()
            lineLength = len(prevModifiedDateStr)

            file.seek(0)

            if lineLength >= 24:
                if prevModifiedDateStr[:24] == CurrentModifiedTime:
                    booleanRunProgram = False

                else:
                    file.truncate(0)
                    file.write(CurrentModifiedTime)

            else:
                file.truncate(0)
                file.write(CurrentModifiedTime)

    # If file does not exist, create a file and write the given latest date.
    else:
        with open(PATH, 'w+') as file:
            file.write(CurrentModifiedTime)

    return booleanRunProgram


def runMain():
    booleanRunProgram = getIsPrevModifiedDateChanged()
    if booleanRunProgram == True:
        import mainSource.Thresholds_Alerts_V2 as thresholdsAlerts
        thresholdsAlerts.main()


runMain()


# # # ***************************************************
# # # Test/Debugging Methods
# # # ***************************************************


def test_getLastModifiedTime():
    PATH = getDataDirectoryForAnalysis()

    lastModifiedTime = getLastModifiedTime(PATH)
    print(lastModifiedTime)


def test_getIsPrevModifiedDateChanged():
    booleanRunMain = getIsPrevModifiedDateChanged()
    print(booleanRunMain)


# # # ***************************************************
# # # Test/Debugging Cases
# # # ***************************************************

# # Uncomment each method call that needs to be tested.
# # NOTE: Do not test more then one method at once
# --------------------------------------------------------


# # Test/Debugging: Get the last modified date for the directory/folder.
# *************************************************

# test_getLastModifiedTime()


# # Test/Debugging: Get boolean result of if the file has been changed.
# *************************************************

# test_getIsPrevModifiedDateChanged()







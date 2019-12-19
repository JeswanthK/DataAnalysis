
"""
    Title:  FCA Competitive Messaging
    Class:  CSC 4996 Senior Project
    Date:   November 25, 2019


"""


# Python Libraries
# -------------------------------------------------
import os
import glob
import pandas as pd
import sys

sys.path.append('../')


# .env file for PATH to get the data location
# -------------------------------------------------
from common.path_to_use import *


def getReadFilesDirectory(PATH):
    """
    Takes in a directory PATH and returns all the files directory path within the
    PATH directory.

    :param PATH: Where to get the data files from
    :return: All the files directory in the given PATH
    """

    if os.path.exists(PATH):
        readFilesDirectory = glob.glob(os.path.join(PATH, "*"))
    else:
        print(PATH, " is not accessible. \nPlease check the directory path ~= Line 35")
        print("File: Concat_all_CSV_Files_In_One_CSV.py")
        exit()

    return readFilesDirectory


def getAllCSVFileDirOEM(PATH):
    """
    readFilesDirectory consists of all the files with the given PATH directory.
    The data for OEM includes some Endemic files which we need to remove to concatenate
    only the OEM data files. This method removes the files that belongs to Endemic.

    :param PATH: Where to get the data files from
    :return: All the files directory in the given PATH
    """

    listOfFileDirectoryToUse = []
    ignoreGoogle = "GOOGLE"
    ignoreEdmund = "EDMUND"

    # Get all the files directory within the given PATH
    readFilesDirectory = getReadFilesDirectory(PATH)

    # If file directory include files from Endemic data, then ignore concatenating those files.
    for file in readFilesDirectory:
        if ignoreGoogle in file:
            continue
        elif ignoreEdmund in file:
            continue

        listOfFileDirectoryToUse.append(file)

    return listOfFileDirectoryToUse


def getAllCSVFileConcatInOne(listOfFileDirectoryToUse, PATH_TO_SAVE):
    """
    Receives list of files that needs to be concatenated and after concatenation, save
    the data frame PATH_TO_SAVE directory.

    :param listOfFileDirectoryToUse: All the files directory that needs to  be concatenated
    :param PATH_TO_SAVE: Where to save the concatenated data file
    :return: None
    """

    allFilesData = []
    csv = ".csv"
    xlsx = ".xlsx"

    # Create a pandas data frame for each file in the directory and append that data frame
    # to a list.
    for eachFileDirectory in listOfFileDirectoryToUse:
        if csv in eachFileDirectory:
            filesData = pd.read_csv(eachFileDirectory, header=0)
        elif xlsx in eachFileDirectory:
            filesData = pd.read_excel(eachFileDirectory, header=0)

        allFilesData.append(filesData)

    # Concatenate the list of all the Pandas data frame into one data frame.
    fileConcat = pd.concat(allFilesData, ignore_index=True)

    fileConcat.to_csv(PATH_TO_SAVE, index=False)






# # # ***************************************************
# # # Test/Debugging Methods
# # # ***************************************************


def test_getReadFilesDirectory():
    PATH = getEndemicDataPath()
    readFilesDirectory = getReadFilesDirectory(PATH)
    print(readFilesDirectory)


def test_getAllCSVFileDirOEM():
    PATH = getOEMDataPath()
    listOfFileDirectoryToUse = getAllCSVFileDirOEM(PATH)
    print(listOfFileDirectoryToUse)


def test_OEM_getAllCSVFileConcatInOne():
    PATH = getOEMDataPath()
    PATH_TO_SAVE = str(getSaveToOEMConcatPath())

    listOfFileDirectoryToUse = getAllCSVFileDirOEM(PATH)
    getAllCSVFileConcatInOne(listOfFileDirectoryToUse, PATH_TO_SAVE)


def test_Endemic_getAllCSVFileConcatInOne():
    PATH = getEndemicDataPath()
    PATH_TO_SAVE = str(getSaveToEndemicConcatPath())

    listOfFileDirectoryToUse = getReadFilesDirectory(PATH)
    getAllCSVFileConcatInOne(listOfFileDirectoryToUse, PATH_TO_SAVE)


# # # ***************************************************
# # # Test/Debugging Cases
# # # ***************************************************

# # Uncomment each method call that needs to be tested.
# # NOTE: Do not test more then one method at once
# --------------------------------------------------------


# # Test/Debugging Get All Files In The Directory
# *************************************************

# test_getReadFilesDirectory()


# # Test/Debugging Get All Files In The Directory That is only for OEM
# *************************************************

# test_getAllCSVFileDirOEM()


# # Test/Debugging Concatenating All OEM Files
# *************************************************

# test_OEM_getAllCSVFileConcatInOne()


# # Test/Debugging Concatenating All Endemic Files
# *************************************************

# test_Endemic_getAllCSVFileConcatInOne()


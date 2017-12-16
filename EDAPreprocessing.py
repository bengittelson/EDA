#parse command-line arguments (or .txt settings file input):
    #path to where .wav files are saved
    #path to where new .wav, .txt, and .TextGrid files should be saved
    #metadata filename
    #metadata variable(s) that you're trying to isolate
    #Google Drive login credentials

import json
import csv
import argparse
import re
import sys
import pandas as pd




def getFileNames(metadata, metadataVars, wavPath):
    #POSSIBLE LINK FOR HOW TO TAKE IN METADATA VARS: https://stackoverflow.com/questions/18608812/accepting-a-dictionary-as-an-argument-with-argparse-and-python

    #store fileNames as a dictionary of file names and phrases
    relFiles = []
    #read in csv file as data frame
    data = pd.read_csv(metadata)
    #loop through metadataVars to create string of variable-value pairs that you want to query
    myQuery = ''
    #use df.query(aforementioned string) to get relevant rows, per this link: https://stackoverflow.com/questions/17071871/select-rows-from-a-dataframe-based-on-values-in-a-column-in-pandas
    # df.loc[df]

    items = metadataVars.items()
    for i in range(0, len(items)): 
        print items[i]
        if 


        # if iterator.hasnext(): 
        #     add = key + " == " + value + " | "
        # else: 
        #     add = key + " == " + value
        # myQuery += add
        # print "myQuery: " + myQuery

    # data.query(myQuery)


    # with open(metadata, 'r') as file:
    #     reader = csv.reader(file)

    #     # # correct for zero-indexing
    #     # phrase_location = phrase_location - 1
    #     # id_location = id_location - 1

    #     for row in reader:
    #         for key, value in metadataVars:
    #             #USE PANDAS HERE TO ACCESS VARIABLES DIRECTLY RATHER THAN ITERATING THROUGH ROWS
    #             #pandas stackoverflow link: https://stackoverflow.com/questions/17071871/select-rows-from-a-dataframe-based-on-values-in-a-column-in-pandas

    #             #create query string

    #             pass

    return relFiles

#function: get file names--return as list
#function: make .txt files

# makes the new file and writes the text to it
def makeNewFiles(newFileName, phrase):
    # extract the identifier from the file name column
    fixedFileName = re.sub('.wav|recordings/', '', newFileName)
    fixedFileName += ".txt"

    # make the new file
    outfile = open(fixedFileName, 'w')

    # print the phrase to the new file
    outfile.write(phrase)
    return fixedFileName

#function: download relevant files from Google drive using list of file names
#function: use WebMAUS API to create TextGrid files for .wav files that don't already have an associated .TextGrid
#call Praat script to segment out specific words using http://www.fon.hum.uva.nl/praat/manual/Scripting_6_9__Calling_from_the_command_line.html

def main():

    # parser = argparse.ArgumentParser(description='Run preprocessing for EDA data.')
    # parser.add_argument('wavPath', metavar='wavPath', type=str, help='the path to the directory where your .wav files '
    #                                                                  'are stored')
    # parser.add_argument('outPath', metavar='outPath', type=str, help='the path to the directory where you want your '
    #                                                                  'output files stored')
    # parser.add_argument('metadata', metavar='metadata', type=str, help='the name of your metadata file')
    # parser.add_argument('metadataVars', metavar='metadataVars', type=str, help='the variables and values by which '
    #                                                                                  'you want to filter')
    #
    #
    # #add Google Drive credentials
    # # parser.add_argument('Google ')
    # args = parser.parse_args()
    #
    # #assign command-line arguments to variables:
    # wavPath = args.wavPath
    # outPath = args.outPath
    # metadata = args.metadata
    # metadataVars = json.loads(args.metadataVars)
    #"/Users/benjamingittelson/Documents/BAAP/BAAP Python Scripts/TestBatch" "/Users/benjamingittelson/Documents/BAAP/BAAP Python Scripts/TestRun" export_recordings_full_V3.csv "{'Ethnicity': 'Other', 'Gender': 'Female'}"

    #parse settings
    settingsFile = sys.argv[1]
    settings = json.load(open(settingsFile))

    wavPath = settings['wavPath']
    metadata = settings['metadata']
    outPath = settings['outPath']
    metadataVars=settings['metadataVars']

    getFileNames(metadata, metadataVars, wavPath)

main()
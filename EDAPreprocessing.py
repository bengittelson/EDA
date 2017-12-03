#parse command-line arguments (or .txt settings file input):
    #path to where .wav files are saved
    #path to where new .wav, .txt, and .TextGrid files should be saved
    #metadata filename
    #metadata variable(s) that you're trying to isolate
    #Google Drive login credentials

import sys
import csv
import argparse
import re

def main():

    parser = argparse.ArgumentParser(description='Run preprocessing for EDA data.')
    parser.add_argument('wavPath', metavar='wavPath', type=str, help='the path to the directory where your .wav files '
                                                                     'are stored')
    parser.add_argument('outPath', metavar='outPath', type=str, help='the path to the directory where you want your '
                                                                     'output files stored')
    parser.add_argument('metadata', metavar='metadata', type=str, help='the name of your metadata file')
    parser.add_argument('metadata variables', metavar='metadataVars', type=str, help='the name of your metadata file',
                        nargs='*')

    #add Google Drive credentials
    # parser.add_argument('Google ')

    args = vars(parser.parse_args())

    for key in args:
        print key
        if key == 'wavPath':
            wavPath = args[key]

    print wavPath



main()


def getFileNames(metadata, metadataVars, wavPath):

    #store fileNames as a dictionary of file names and phrases
    relFiles = []
    with open(metadata, 'r') as file:
        reader = csv.reader(file)

        # # correct for zero-indexing
        # phrase_location = phrase_location - 1
        # id_location = id_location - 1

        for row in reader:
            #store metadataVars as a dictionary of variables and values?
            for var in metadataVars:
                #iterate to that variable column and check if the values match
                pass

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


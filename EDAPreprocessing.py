#parse command-line arguments (or .txt settings file input):
    #path to where .wav files are saved
    #path to where new .wav, .txt, and .TextGrid files should be saved
    #metadata filename
    #metadata variable(s) that you're trying to isolate
    #Google Drive login credentials

import sys
import argparse

def main():
    settings = sys.argv

    #WORK ON ON ARGPARSER
    parser = argparse.ArgumentParser(description='Run preprocessing for EDA data.')
    parser.add_argument('wavPath', metavar='wavPath', type=str, help='the path to the directory where your .wav files '
                                                                     'are stored')

    parser.add_argument('outPath', metavar='outPath', type=str, help='the path to the directory where you want your '
                                                                     'output files stored')

    args = parser.parse_args()
    print args
    # print settings


main()


#function: get file names--return as list
#function: make .txt files
#function: download relevant files from Google drive using list of file names
#function: use WebMAUS API to create TextGrid files for .wav files that don't already have an associated .TextGrid
#call Praat script to segment out specific words using http://www.fon.hum.uva.nl/praat/manual/Scripting_6_9__Calling_from_the_command_line.html


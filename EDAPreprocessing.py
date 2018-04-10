#parse command-line arguments (or .txt settings file input):
    #path to where .wav files are saved
    #path to where new .wav, .txt, and .TextGrid files should be saved
    #metadata filename
    #metadata variable(s) that you're trying to isolate
    #Google Drive login credentials

from __future__ import print_function
import json
import csv
import argparse
import re
import sys
import pandas as pd
from os import path, listdir, rename, remove
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

#getFiles (return entire rows from dataframe)
#makeNewFiles (return just a list of the file names)
#download from Google Drive



def getFiles(metadata, metadataVars, wavPath):
    #store fileNames as a dictionary of file names and phrases
    relFiles = []
    #read in csv file as data frame
    data = pd.read_csv(metadata)
    relFiles = data.query(metadataVars)
    return relFiles

#function: get file names--return as list
#function: make .txt files


#take in list of files from getFiles and metadata file
def tagComplete(relFiles, data):
    #cast to set for faster membership checking
    relSet = relFiles['recording']
    relSet = set(relSet)
    #print(relSet)
    data['in_first_batch'] = False
    for i, row in data.iterrows(): 
        if row['recording'] in relSet: 
            data.loc[i, 'in_first_batch'] = True
    
    #print(data[:100])


# makes the new file and writes the text to it
def makeNewFiles(files, wavPath, outPath):
    wavFiles = set(listdir(wavPath))
    # print(files)

    # extract the identifier from the file name column
    for row in files: 
        curRow = next(files.iterrows())[1]
        print(curRow['recording'])
        recCheck = re.sub('recordings/', '', curRow['recording'])
        # print(recCheck)

        #check if there's a corresponding recording in the folder; if not, do nothing
        if recCheck in wavFiles: 
            phrase = curRow['phrase']
            # print(recording)
            newFileName = re.sub('.wav|recordings/', '', recCheck)
            newFileName += ".txt"
            # print(newFileName)

            # make the new file
            outfile = open(path.join(outPath, newFileName), 'w')
            print(str(path.join(outPath, newFileName)))


            # print the phrase to the new file
            print(phrase + ': ' + wavPath + newFileName)
            outfile.write(phrase)

            #move the corresponding wav file: 
            rename(path.join(wavPath, recCheck), path.join(outPath, recCheck))
            print(str(path.join(wavPath, recCheck)) + " -> " + str(path.join(outPath, recCheck)))
            #return fixedFileName

#function: download relevant files from Google drive using list of file names
#function: use WebMAUS API to create TextGrid files for .wav files that don't already have an associated .TextGrid
#call Praat script to segment out specific words using http://www.fon.hum.uva.nl/praat/manual/Scripting_6_9__Calling_from_the_command_line.html


def fixWavNames(wavPath): 
    for file in listdir(wavPath): 
        match = re.search(r".*\"$", file)

        hidden = file.startswith("._")

        #if a match and NOT a hidden file
        if match and not hidden: 
            print(file)
            fixedFileName = re.sub('\"', '', file)
            print(fixedFileName)
            rename(path.join(wavPath, file), path.join(wavPath, fixedFileName))


#remove hidden files
def removeHiddenFiles(wavPath): 
    for file in listdir(wavPath): 
        if file.startswith("._"): 
            print(file) 
            remove(path.join(wavPath, file))

#make unique identifier for each for each speaker: 
def makeID(data): 
    
    #add a new column for the identifiers
    identifier = 0

    #set all identifiers equal to -1
    data['identifier'] = -1

    #for each row in the file: https://stackoverflow.com/questions/23330654/update-a-dataframe-in-pandas-while-iterating-row-by-row/29262040
    for i, row in data.iterrows(): 
        #if the phrase is "There once was..."
        breakPhrase = "There was once a poor shepherd boy who used to watch his flocks in the fields next to a dark forest near the foot of a mountain."
        if row['phrase'] == breakPhrase: 
            identifier = identifier + 1

        #set the value: https://stackoverflow.com/questions/16729574/how-to-get-a-value-from-a-cell-of-a-dataframe
        data.loc[i, 'identifier'] = identifier

    #print(data[:100])
    data.to_csv('data_with_ids.csv')
    return data

#download from Google Drive
def downloadFiles(files, APIkey): 
    #boilerplate authorization: http://wescpy.blogspot.com/2014/09/simple-google-api-access-from-python.html
    SCOPE = "https://www.googleapis.com/auth/drive"

    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPE)
        creds = tools.run_flow(flow, store)

    API_KEY = APIkey
    #GDRIVE = discovery.build('drive', 'v3', developerKey = API_KEY)
    GDRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

    for file in files: 
        #
        file_id = '0B_QwHTyWgOHCbWNhX19pSERDaHc'
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print ("Download %d%%." % int(status.progress() * 100))




def main():
    #parse settings
    settingsFile = sys.argv[1]
    settings = json.load(open(settingsFile))

    wavPath = settings['wavPath']
    metadata = settings['metadata']
    outPath = settings['outPath']
    metadataVars=settings['metadataVars']
    APIkey = settings['APIkey']

    data = pd.read_csv(metadata)
    makeID(data)

    rel = getFiles(metadata, metadataVars, wavPath)
    #fixWavNames(wavPath)
    #removeHiddenFiles(wavPath)
    makeNewFiles(rel, wavPath, outPath)
    tagComplete(rel, data)
    data.to_csv('data_with_tags_and_ids.csv')
    
    #downloadFiles(APIkey, files)

main()
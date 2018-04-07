#Ben Gittelson
#Preprocessing for British English app corpus
#March 2, 2016

import csv
import re
import os
import shutil

def main(): 
    print "Welcome to FileMaker. Press CTRL + C to exit this program at any \
time."
    
    #get preliminary user input
    myPath = raw_input("Please input the path of the folder where you want to \
save the new files.")
   
    #check whether the user has entered a valid path 
    again3 = True
    while again3: 
        try: 
            makeNewDir(myPath)
            again3 = False
        except OSError: 
            myPath = raw_input("Sorry, that folder already exists. Please type \
in a path to a new folder.")

    #set the working directory variable
    workingDirectory = os.getcwd()
    
    wavPath = raw_input("Please input the path of the folder where you have \
your .wav files saved.")
    #check whether the user has entered a valid directory name
    again = True
    while again: 
        if os.path.isdir(wavPath): 
            again = False
        else: 
            wavPath = raw_input("Sorry, I couldn't find that folder. Please \
type in the folder path again.")
         
    #check whether the user has entered a valid metadata filename   
    infile_name = raw_input("Please input the name of the file you want to \
process.")
    again2 = True
    while again2: 
        if os.path.isfile(infile_name): 
            again2 = False
        else: 
            infile_name = raw_input("Sorry, I couldn't find that file. Please \
type in the file name again.")
        
    phrase_choice = raw_input("Please type in the sentence you want to use.")
            
    phrase_location = input("Please type in the number of the column where \
the phrase you're searching for is located as an integer. That is, if \
the phrase is written in the first column of the data file, type '1', \
and if it is in the second column, type '2', et cetera.")
    
    id_location = input("Please type in the number of the column where the \
file ID you're searching for is located as an integer. That is, if the \
file ID is written in the first column of the data file, type '1', and \
if it is in the second column, type '2', et cetera.")
    
    #make the new files
    getFileNames(phrase_location, id_location, infile_name, phrase_choice, 
    workingDirectory, myPath, wavPath)

#takes in user input collected above and makes new .txt files in the specified
# folder
def getFileNames(phrase_location, id_location, infile_name, phrase_choice, pwd, 
myPath, wavPath): 
   with open(infile_name, 'r') as file: 
        reader = csv.reader(file)
        
        #correct for zero-indexing
        phrase_location = phrase_location - 1
        id_location = id_location - 1
        
        for row in reader: 
            if row[phrase_location] == phrase_choice:                
                #move the .wav files
                try: 
                    wavName = re.sub('recordings/', '', row[id_location])
                    newWavPath = myPath + "/" + wavName
                    currentWavPath = wavPath + "/" + wavName
                    moveFile(currentWavPath, newWavPath)
                    
                    #make the new .txt file and set its name = newPath
                    newName = makeNewFiles(row[id_location], phrase_choice)
                    newTxtPath = myPath + "/" + newName
                    currentTxtPath = pwd + "/" + newName
                    moveFile(currentTxtPath, newTxtPath)   
                except IOError: 
                    print "Sorry, I couldn't find a file called " + newWavPath


#makes the new file and writes the text to it
def makeNewFiles(newFileName, phrase): 
    #extract the identifier from the file name column
    fixedFileName = re.sub('.wav|recordings/', '', newFileName)
    fixedFileName += ".txt"
    
    #make the new file
    outfile = open(fixedFileName, 'w')
    
    #print the phrase to the new file
    outfile.write(phrase)
    return fixedFileName

#make new directory
def makeNewDir(path): 
    os.mkdir(path, 0755) 

#move files from the old location to the new location
def moveFile(oldPath, newPath): 
    shutil.move(oldPath, newPath)

main()








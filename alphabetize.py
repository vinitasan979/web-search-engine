'''
Names: Vincent Vu(27117314/vmvu1), Vinita Santhosh(51795233/santhosv) , Kinjal Reetoo (36923637.kreetoo)
Professor Cristina Lopes
CS121
Project 3: alphabetize
3 December 2019
'''
import ast
import os
import pickle

def main():
    # Start of reading final merged dict
    # Try/except, for when the tokens file runs out
    try:
        # Opens up "tokens.txt" for reading, establishes an offset dictionary
        inputFile = open(os.path.dirname(__file__) + '/Tokens.txt', "r")
        offset = {}
        # Sets up the first line, and a placeholder startingLetter(used for checking)
        currentLine = ast.literal_eval(inputFile.readline())
        startingLetter = "0"

        # used to loop through all letters of the alphabet
        alphabetList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

        # Starts off writing the misc file, since sorted sorts numbers first(will write all keys and their dictionaries in the file)
        indexFile = open((os.path.dirname(__file__) + '/Index Folder/misc.txt'), "w+", encoding="utf-8")

        # While the first character of the key does not start with a letter, write it out into the misc file
        while (ord(startingLetter) < 97 or ord(startingLetter) > 122):
            # Gets the key in currentLine, and assign the key to its offset number to its offset
            key = next(iter(currentLine))
            offset[key] = indexFile.tell()

            # Manual writing of the line in dictionary form

            indexFile.write("{" + "\"" + str(key) + "\": " )#+ str(currentLine[key]) + "}\n")

            # Sets up the next line, and
            currentLine = ast.literal_eval(inputFile.readline())
            startingLetter = next(iter(currentLine))[0]
        indexFile.close()

        # Start of all letters
        for letter in alphabetList:
            indexFile = open((os.path.dirname(__file__) + '/Index Folder/' + letter + '.txt'), "w+", encoding="utf-8")

            # While the first character of the key starts with letter, add that line to the letter's file
            while (startingLetter == letter):
                # Gets the key in currentLine, and assign the key to its offset number to its offset
                key = next(iter(currentLine))
                offset[key] = indexFile.tell()
                top_tier={}
                top_tier[key]={}
                index_count=0
                for k,val in currentLine[key].items():
                    if(index_count<15000):
                        top_tier[key][k]=val
                        index_count+=1
                    else:
                        break


                # Manual writing of the line in dictionary form
                indexFile.write("{" + "\"" + str(key) + "\": " + str(top_tier[key]) + "}\n")



                # Sets up the next line, and
                line=inputFile.readline()
                currentLine = ast.literal_eval(line)
                startingLetter = next(iter(currentLine))[0]
            indexFile.close()

    # When the file runs out of lines, close inputFile and continue
    except:
        inputFile.close()

    # Creates the pickle file for pickle dump. Stores offset in Index Folder
    off = open((os.path.dirname(__file__) + '/Index Folder/offset.pkl'), "wb+")
    pickle.dump(offset, off)
    off.close()


if __name__ == "__main__":
    main()

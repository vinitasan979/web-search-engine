'''
Names: Vincent Vu(27117314/vmvu1), Vinita Santhosh(51795233/santhosv) , Kinjal Reetoo (36923637.kreetoo)
Professor Cristina Lopes
CS121
Project 3: M1
3 December 2019
'''
import os
import json
from bs4 import BeautifulSoup
import re
from nltk.stem import PorterStemmer
import merge_Files
import alphabetize
import math

#Declaration of a simple exception to get out of a bunch of nested structures(This is more for testing)
class GetOutOfLoop(Exception):
    pass

#Function gets the tf score for each token in a document, arguments are the tokens dict, the words in a doc, and the unique number assigned to the doc's url
def tf_score(tokens,doc_count,jsonCount):
    #For each key in the tokens dictionary, assign the url's tf score(if everything exists)
    for key in tokens:
        try:
            tokens[key][jsonCount] = (1 + math.log(float(tokens[key][jsonCount])))# / float(doc_count)))
        except KeyError:
            pass
    return tokens

def main():
    #Try for the GetOutOfLoop error
    try:
        #Initializes the tokens dictionary, and jsonCounter(unique url assignment counter), and opens the doc ID file
        tokens = {}
        jsonCounter = 0
        docID_file = open('docIDs.txt', "w+", encoding="utf-8")

        #NOTE: Change this when we want to change the number of files to search through(normal number is 55393)
        size = 55393

        #Change into the directory that is being read
        os.chdir(os.path.abspath("./DEV"))

        #For each directory in the DEV directory
        for directory in os.listdir("."):
            #Make sure that the directory is actually a directory
            if os.path.isdir(os.path.abspath(directory)):
                #Moves into that directory
                os.chdir(os.path.abspath(directory))

                #For each file in the directory, if the file is a json file, it will open it and read it
                for file in os.listdir(os.path.abspath(".")):
                    #Cbecks if the item inside of the directory is a file
                    if os.path.isfile(os.path.abspath(file)):
                        #Testing print statements

                        #Reads the json and increments counter of json files
                        with open(os.path.abspath(file), "r") as read_file:
                            #Initializing variables needed for tokenizing the word
                            data = json.load(read_file)
                            soup = BeautifulSoup(data["content"], "html.parser")
                            ps = PorterStemmer()
                            word_count_per_doc = 0

                            #Increments jsonCounter, since this file was able to be opened
                            jsonCounter += 1
                            print(directory)
                            print(jsonCounter, file)

                            #Checks for important words. Increments the url's frequency by 5 if there is an important word
                            for w in soup.find_all(["h1","h2","h3","strong","title"]):
                                for s in (re.split(r'([a-zA-Z0-9_]+)', str(w.get_text()))):
                                    if (bool(re.match('^[a-zA-Z0-9_]+$', str(s)))):
                                        stem = ps.stem(str(s)).lower()

                                        #Checks if a word doesn't exist in the tokens dictionary.
                                        #If so, make a new one, and assign the url's number to be 5
                                        if tokens.get(stem) is None:
                                            tokens[stem] = {}
                                            tokens[stem][jsonCounter] = 5.0
                                        #If the word already exists, check to see if the url isn't in that word's dictionary.
                                        #If it is not, assign it to 5. Otherwise, increment by 5
                                        else:
                                            if tokens[stem].get(jsonCounter) is None:
                                                tokens[stem][jsonCounter] = 5.0
                                            else:
                                                tokens[stem][jsonCounter] += 5.0

                            #Checks for any word, and increases the frequency by 1
                            for word in list(soup.strings):
                                for w in (re.split(r'([a-zA-Z0-9_]+)', word)):
                                    if bool(re.match('^[a-zA-Z0-9_]+$', w)):
                                        if(all(ord(char) < 128 for char in 'w')):
                                            if ((w.isdigit() and len(w)<=4) or not w.isdigit()):
                                                 stem_word=ps.stem(w).lower()
                                                 word_count_per_doc += 1
                                                 if tokens.get(stem_word) is None:
                                                     tokens[stem_word] = {}
                                                     tokens[stem_word][jsonCounter] = 1.0

                                                 else:
                                                     if (tokens[stem_word].get(jsonCounter) is None):
                                                         tokens[stem_word][jsonCounter] = 1.0
                                                     else:
                                                         tokens[stem_word][jsonCounter] += 1.0


                    #calculate tf score for each term in doc
                    tokens = tf_score(tokens, word_count_per_doc, jsonCounter)

                    #Code for chunking and merging

                    #First chunk
                    if (jsonCounter == 18464):
                        #Sorts the dictionary, and make a new index file
                        tokens = dict(sorted(tokens.items()))
                        indexDump = open((os.path.dirname(__file__) + '/firstIndex.txt'), "w+")
                        print("HERE")
                        #Writes out each key and the key's dictionary in the tokens dictionary
                        for key in list(tokens):
                            indexDump.write("{" + '"' + key + '"' + " :" + str(dict(sorted(tokens[key].items()))) + "}\n")

                        #Closes the indexDump file, and empties the token dictionary for the next chunk
                        indexDump.close()
                        tokens = {}

                        #Second chunk
                    elif (jsonCounter == 36928):
                        # Sorts the dictionary, and make a new index file
                        tokens = dict(sorted(tokens.items()))
                        indexDump = open((os.path.dirname(__file__) + '/secondIndex.txt'), "w+")

                        # Writes out each key and the key's dictionary in the tokens dictionary
                        for key in list(tokens):
                            indexDump.write("{" + '"' + key + '"' + " :" + str(dict(sorted(tokens[key].items()))) + "}\n")

                        #Closes the indexDump file, and empties the token dictionary for the next chunk
                        indexDump.close()
                        tokens = {}

                        #Third chunk, and gets out of the loop
                    elif jsonCounter == 55393:

                        #Does a final write without \n, since it's the last
                        docID_file.write(data["url"])
                        docID_file.close()

                        tokens = dict(sorted(tokens.items()))
                        new_path = (os.path.dirname(__file__) + '/thirdIndex.txt')
                        IndexDump = open(new_path, "w+")
                        for key in list(tokens):
                            IndexDump.write("{" + '"' + key + '"' + " :" + str(dict(sorted(tokens[key].items()))) + "}\n")

                        # Closes the indexDump file, and empties the token dictionary to remove it from memory
                        IndexDump.close()
                        tokens = {}

                        raise GetOutOfLoop

                    #Writes the url to docID_file at the jsonCounter
                    docID_file.write(data["url"]+"\n")
                os.chdir("..")

    #Returns back to the project directory
    except GetOutOfLoop:
        os.chdir("..")
        os.chdir("..")

    #Merges all of the indicies together, and gets the new tf-idf scores for each token
    merge_Files.merge(jsonCounter)

    #Makes 27 index files(one for each letter of the alphabet, and then one for tokens that don't start with a letter)
    alphabetize.main()

if __name__ == "__main__":
    main()

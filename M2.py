'''
Names: Vincent Vu(27117314/vmvu1), Vinita Santhosh(51795233/santhosv) , Kinjal Reetoo (36923637.kreetoo)
Professor Cristina Lopes
CS121
Project 3: M2
19 November 2019
'''
from nltk.stem import PorterStemmer
import re
import pickle as pkl
import os
import ast
import math
from collections import defaultdict
import time

import operator
import linecache

#Main Driver
def main():
    #Sets up input and stemmer, as well as compiling
    userInput = ""
    ps = PorterStemmer()
    reSplit = re.compile(r'([a-zA-Z0-9_]+)')
    reMatch = re.compile('^[a-zA-Z0-9_]+$')
    reDict = re.compile(r'{|}|,')

    #Changes into the Index Folder directory
    os.chdir("Index Folder")

    #Sets up the offset dictionary
    offsetFile = open("offset.pkl", "rb")
    offsetDict = pkl.load(offsetFile)
    offsetFile.close()

    doc_file=open(os.path.dirname(__file__) +"/doc_lengths.pkl","rb")
    doc_lengths=pkl.load(doc_file)
    doc_file.close()
   # print("doc lengths -> ",doc_lengths)

    afile = open("a.txt")
    bfile = open("b.txt")
    cfile = open("c.txt")
    dfile = open("d.txt")
    efile = open("e.txt")
    ffile = open("f.txt")
    gfile = open("g.txt")
    hfile = open("h.txt")
    ifile = open("i.txt")
    jfile = open("h.txt")
    kfile = open("k.txt")
    lfile = open("l.txt")
    mfile = open("m.txt")
    nfile = open("n.txt")
    ofile = open("o.txt")
    pfile = open("p.txt")
    qfile = open("q.txt")
    rfile = open("r.txt")
    sfile = open("s.txt")
    tfile = open("t.txt")
    ufile = open("u.txt")
    vfile = open("v.txt")
    wfile = open("w.txt")
    xfile = open("x.txt")
    yfile = open("y.txt")
    zfile = open("z.txt")
    miscfile = open("misc.txt")

    indexes = {
    "a": afile,
    "b": bfile,
    "c": cfile,
    "d": dfile,
    "e": efile,
    "f": ffile,
    "g": gfile,
    "h": hfile,
    "i": ifile,
    "j": jfile,
    "k": kfile,
    "l": lfile,
    "m": mfile,
    "n": nfile,
    "o": ofile,
    "p": pfile,
    "q": qfile,
    "r": rfile,
    "s": sfile,
    "t": tfile,
    "u": ufile,
    "v": vfile,
    "w": wfile,
    "x": xfile,
    "y": yfile,
    "z": zfile,
    "misc": miscfile }


    #while True loop, that will keep running until the user enters "exit~"
    while True:
        # Gets query from user, and also sets up a list of words for the query
        userInput = input("Please enter a query(enter \"exit~\" to exit program): ").lower().strip()
        start = time.time()
        listOfWords = []

        # If the user entered "exit~"
        if userInput == "exit~":
            return

        # Splits up the user input to make the listOfWords

        for word in (re.split(reSplit, userInput)):
            if re.match(reMatch, word):
                listOfWords.append(ps.stem(word))


        query_vector = {}
        scores = defaultdict(float)

        for word in listOfWords:
            if offsetDict.get(word) is not None:
                offset = offsetDict[word]
                letter = word[0]
                if letter.isdigit() or letter=="_":
                    indexFile = indexes["misc"]
                else:
                    indexFile = indexes[letter]
                indexFile.seek(offset)
                line = indexFile.readline().strip()
                query_dict = eval(line)



                query_vector[word] = ( math.log(float(55393) / len(listOfWords))) * (1+ math.log(1/len(query_dict)))
                file_count=0
                keys=list(query_dict[word].keys())
                #print(query_dict[word])
                for key in keys:
                        scores[key] += (scores[key] * query_vector[word])
                    #else:
                         #print("done with file count")
                         #break

        for doc in scores:
            scores[doc]=scores[doc]/(math.sqrt(doc_lengths[doc]))

        for topk in sorted(scores, key = scores.get, reverse=True)[:5]:
                #print("topk",topk)
                print(linecache.getline("docIDs.txt", int(topk)))
        end = time.time()
        print("TIME", end - start)




if __name__ == "__main__":
    main()

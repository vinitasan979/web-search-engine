import math
import ast
import os
from collections import defaultdict
import pickle
total_wgt=defaultdict(float)

def tf_idf_score(tok, N,cur_word):
    global total_wgt
    idf = math.log(float(N) / len(tok[cur_word].keys())) #total number of document / total no.of docs with the word
    for k in tok[cur_word].keys():
            tfidf= tok[cur_word][k] * idf
            tok[cur_word][k] =tfidf
            total_wgt[k]+=((tfidf)**2)
    return(tok)

def minimum(word_cmp):
    small=min(word_cmp)
    pos = []
    for word in range(len(word_cmp)):
        if word_cmp[word]==small:
            pos.append(word)
    return(pos)
def merge(N):

    f1=open((os.path.dirname(__file__) +'/firstIndex.txt'),'r')
    f2=open((os.path.dirname(__file__) + '/secondIndex.txt'),'r')
    f3=open((os.path.dirname(__file__)+ '/thirdIndex.txt'),'r')
    files=[f1,f2,f3]

    output_file=os.path.dirname(__file__) + '/Tokens.txt'
    token=open(output_file,'w')
    cmp=[]
    for item in files: #set up cmp list
        word=item.readline()
        if word=='': #if file has no words
            files.pop(files.index(item))
        else:
            cmp.append(ast.literal_eval(word))
    #print("inital setup ",cmp)
    while(len(files)!=0):
        #print("current length of files ",len(files))
        word_cmp=[] #list of just the words
        for wno in range(len(cmp)):
            key=list(cmp[wno].keys())[0]
            word_cmp.append(key)
            wno += 1
        pos=minimum(word_cmp) #find the smallest word
        #writing out to file
        main_dict=cmp[pos[0]]
        #merge if needed

        num=0
        cur_word=word_cmp[pos[0]]
        while(num<len(pos)):
            if(num!=0):
                for key,val in cmp[pos[num]][cur_word].items():
                    main_dict[cur_word][key]=val
            new_word = files[pos[num]].readline()
            if (new_word ==''or new_word==None or new_word=="\n"):
                files.pop(pos[num])
                cmp.pop(pos[num])
                no=num+1
                while(no<len(pos)):
                    pos[no]=pos[no]-1
                    no+=1
            else:
                cmp[pos[num]] = ast.literal_eval(new_word)
            num+=1
        cur_word=word_cmp[pos[0]]
        #print(list(main_dict[cur_word].keys()))
        main_dict=tf_idf_score(main_dict,N,cur_word)
        sort_dict={}
        sort_dict[cur_word]={}
        #dcount=0
        for key in sorted(main_dict[cur_word], key=main_dict[cur_word].get, reverse=True):
            #if(dcount<10000):
                sort_dict[cur_word][key]=main_dict[cur_word][key]
                #dcount+=1
            #else:
                #break
        #print("final main_dict",main_dict)
        #print("final sorted dict ",sort_dict)
        token.write(str(sort_dict)+'\n')
    doc_len = open(os.path.dirname(__file__) +"/doc_lengths.pkl", "wb")  # creates the pickle file for pickle dump. Stores offset in Index Folder
    pickle.dump(total_wgt, doc_len)
    doc_len.close()















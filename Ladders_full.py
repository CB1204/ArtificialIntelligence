'''
Created on Dec 2, 2017

@author: Christian

Module to implement ladders game as a search problem
'''
import os
import time
import sys

def ladders(inword, outword):
    #finds the shortest path from the inword to the outword.
    
    # first try: efficiently sort all input words (from file) and then try a* search
    # heuristic: number of different letters between word and goal
    
    #read raw data
    worddict=readdatafile()
    #find important specification about the problem
    lettersIn=countletters(inword)[1]
    lettersOut=countletters(outword)[1]

    #initialize search 
    start=wordnode("___0_0",inword,0,sum([abs(lettersIn[i]-lettersOut[i]) for i in range(26)]))
    openlist=[start]
    closedlist=[]
    
    while len(openlist)>0:
        #find currently best f, pop it
        bestf=1e3
        for node in openlist:
            if node.f<bestf:
                #this node is better than the currently best
                bestf=node.f
                bestidx=openlist.index(node)
        activenode=openlist.pop(bestidx)
        
        lenAct=len(activenode.word)
        g=activenode.g+1
        #generate the successors
        
        #all words which have one more or one less letters than the current inword are candidates
        # find candidate solutions
        candidateSolutions=[]
        if str(lenAct-1) in worddict.keys():
            candidateSolutions+=worddict[str(lenAct-1)]
        if str(lenAct+1) in worddict.keys():
            candidateSolutions+=worddict[str(lenAct+1)]
    
        # of the candidate solutions, there will only be few neighbors
        neighbors=[comparewords(word, activenode.letters,lettersOut) for word in candidateSolutions]

        #for each successor, check if it is the goal
        for success,word,h in neighbors:
            if success:
                if word==outword:
                    #this is the solution
                    return getwordpath(closedlist,activenode, word)
                else:
                    #check if the word is already in open/closed list with lower f
                    #this automatically means that g is smaller for this node (no impact on h)
                    #therefore, this node need not be saved
                    inOpenList=[node for node in openlist if node.word==word and node.g<=g]
                    inClosedList=[node for node in openlist if node.word==word and node.g<=g]
                    if not inOpenList and not inClosedList:
                        #add the node to the openlist
                        openlist.append(wordnode(activenode.ID,word,g,h))
                         
        #add the node which was expanded to the closed list
        closedlist.append(activenode)
    #if no goal is found, return error
    return False
          
def getwordpath(listnodes,activenode,word):  
    path=[activenode.word, word]
    while not activenode.parentID=="___0_0":
        for node in listnodes:
            #loop through all nodes
            if node.ID==activenode.parentID:
                #this is the parent of the current node
                #insert the found word 
                path.insert(0,node.word)
                #set the activenode one level up
                activenode=node
        
    return path
                    
def comparewords(word,baselist,targetlist):
    [success,wordlist]=countletters(word, baselist)
    if success:
        if sum([abs(wordlist[i]-baselist[i]) for i in range(26)])==1:
            return [True,word,sum([abs(wordlist[i]-targetlist[i]) for i in range(26)])]
        
    #this is not a valid neighbor
    return [False,word,100]
    
def countletters(word,baselist=[20]*26):
    #counts the letters of word
    #as soon as there are two letters different than the base, it stops and returns true
    listword=[0]*26
    toomuch=0
    for letter in word:
        ordlet=ord(letter)-97
        listword[ordlet]+=1
        if listword[ordlet]>baselist[ordlet]:
            toomuch+=1
        if toomuch>=2:
            return [False,[]]
    return [True,listword]
          
def readdatafile():
    #reads the wordlist.txt file
    cwd = os.getcwd()
    filename=cwd+'\\wordList.txt'
    content=dict()
    with open(filename,'r') as file:
        #this is approx. 20% slower, but still worth the work, as separate classes per size are returned
        for line in file:
            l=str(len(line)-1)
            if l in content.keys():
                content[l].append(line[:-1])
            else:
                content[l]=[line[:-1]]
        #reader = csv.reader(file)
        #lstOut = list(reader)
            
    return content

class wordnode:
    def __init__(self, parentID, word, g,h):
        #takes the parentID, the word and the cost values g and h
        self.parentID=parentID
        self.ID = word+'_'+str(g)+'_'+str(h)
        self.word=word
        self.letters=countletters(word)[1]
        self.f=g+h 
        self.g=g
        self.h=h

        
def testread():
    start=time.perf_counter()
    for i in range(1):
        datalist=readdatafile()
    end = time.perf_counter()
    print(end-start)
    sumlen=0
    for el in datalist.values():
        sumlen+=len(el)
        print(len(el))
    print(sumlen)

def testword():             #  a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z
    print(countletters("word",[1,1,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,0,2,1,0,0,0,0,0,0]))
    print(countletters("test",[0,0,0,0,2,0,0,0,0,0,0,0,0,1,0,0,0,0,1,2,0,0,0,0,0,0]))
    
    print(comparewords("baselis",[1,1,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,0,2,1,0,0,0,0,0,0]))
    print(comparewords("testn",[0,0,0,0,2,0,0,0,0,0,0,0,0,1,0,0,0,0,1,2,0,0,0,0,0,0]))

        
def testperformance_listcomp(dofor):
    start=time.perf_counter()
    a=range(1000,-1,-1)
    bestval=1e3
    for i in range(1):
        #do 1000 loops, just to produce meaningful times
        if dofor:
            for j in a:
                if j<bestval:
                    bestval=j
                    bestidx=a.index(j)
        else:
            j=0
            while True:
                if [x for x in a if x<=j]:
                    bestidx=a.index(j)
                    break
                j+=1

    print(bestidx)
            
    end=time.perf_counter()
    print(end-start)
        
def test_ladders():
    start=time.perf_counter()
    result1=ladders('croissant','baritone')
    end=time.perf_counter()
    print(result1)
    print(end-start)
    
    start=time.perf_counter()
    result2=ladders('crumpet','treacle')
    end=time.perf_counter()
    print(result2)
    print(end-start)
    
    start=time.perf_counter()
    result3=ladders('apple','pear')
    end=time.perf_counter()
    print(result3)
    print(end-start)
    start=time.perf_counter()
    result4=ladders('lead','gold')
    end=time.perf_counter()
    print(result4)
    print(end-start)

#call from shell
solution=ladders(sys.argv[1],sys.argv[2])
#print result to shell
for i in solution:
    print(i)
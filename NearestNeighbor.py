# ====================================================================
# Authors:
# Michael Tucker              tuckemic@oregonstate.edu    ID: 933-194-613
# Philip  Michael Sigillito   sigillip@oregonstate.edu    ID: 932-925-316
# Dominic Wasko               waskod@oregonstate.edu      ID: 932-620-942
# CS325 / Traveling Salesman Project
# Date: 3/16/2018
# Description: Solves the traveling salesman optimization problem
# ====================================================================

# =====================================================================
# Imports
# =====================================================================

import sys
import math
import os
import re
from collections import namedtuple


# =====================================================================
# Objects
# =====================================================================

#Node Struct stores vertices EdgeStruct Stores Edges

#Values : Id Number, X Vertex, Y Vertex
NodeStruct = namedtuple("NodeStruct", "number x y")

#Values: Start Vertex, End Vertex, Weight
EdgeStruct = namedtuple("EdgeStruct", "v1 v2 weight")

# =====================================================================
# Functions
# =====================================================================

#Get Distance Between two nodes rounded to the nearest integer
def getWeight(node1, node2):
    weight = math.hypot(node1.x - node2.x, node1.y - node2.y)
    return int(round(weight))

def getInput(fileName, nodeList):
    thisDirectory = os.path.dirname(os.path.abspath(__file__))
    inputFile = os.path.join(thisDirectory, fileName)
    readTextFile = open(inputFile).read().splitlines()
    for i, val in enumerate(readTextFile):
        val = val.lstrip(' ')
        val = re.sub(' +', ' ', val)
        readTextFile[i] = val.split(' ')
        readTextFile[i] = list(map(int, readTextFile[i]))
    for i, node in enumerate(readTextFile):
        currentNode = NodeStruct(node[0], node[1], node[2])
        nodeList.append(currentNode)
    return nodeList

def saveResults(fileName, nodeList, finalWeight):
    tourFile = fileName + ".tour"
    writeFile = open(tourFile, 'a+')
    writeFile.write("%s" % finalWeight)
    writeFile.write("\n")
    for i, node in enumerate(nodeList):
        writeFile.write("%s" % nodeList[i].number)
        writeFile.write("\n")
    writeFile.close()


def getTotalTourWeight(nodeList):
    nodeCount = len(nodeList)
    totalTourWeight = 0
    for i in range(0, nodeCount - 1):
        totalTourWeight += getWeight(nodeList[i], nodeList[i + 1])
    totalTourWeight += getWeight(nodeList[nodeCount - 1], nodeList[0])
    return totalTourWeight

def printNodeList(nodeList):
    nodeStr = ""
    for node in nodeList:
        nodeStr += str(node.number)
        nodeStr += ", "
    nodeStr2 = nodeStr.rstrip(', ')
    nodeStr2 += "\n"
    print(nodeStr2)
    return nodeStr2

def getArgs():
    global cycleCount, fileName, maxSwaps
    argCount = len(sys.argv)
    if argCount > 2 or argCount < 2:
        print("Invalid argument count. Please follow usage:")
        print("python tsp.py <-cycle count> <file name>")
        print("EX: python tsp.py input.txt")
        exit(1)
    if argCount == 2:
        cycleCount = 3
        fileName = sys.argv[1]
        thisDirectory = os.path.dirname(os.path.abspath(__file__))
        inputFile = os.path.join(thisDirectory, fileName)
        if not os.path.isfile(inputFile):
            print("The file: % could not be found in this directory" % fileName)
            exit(1)

if __name__ == '__main__':

    print("\n***** Main *****\n")

    # the getArgs function uses global variables. Make sure you have these two variable declared before you call it
    fileName = ""
    getArgs()



# =====================================================================
# Nearest Neighbor Code
# =====================================================================
    workingNodeList = []
    getInput(fileName, workingNodeList)
    totalTourWeight = getTotalTourWeight(workingNodeList)

    #create empty result list and put first vertex in it
    newNodeList = []
    newNodeList.append(workingNodeList[0])
    del workingNodeList[0]
    newIndex = 0
    
    print "running alg..."
    #while not all cities have been added
    while (len(workingNodeList) > 0):
        #make shortestDistance unreasonably high so first distance will be set
        shortestDistance = 1000000000
        targetIndex = -1
        #get index of shortest distance
        for i in range(0, len(workingNodeList)):
            distance = getWeight(newNodeList[newIndex], workingNodeList[i] )
            if( distance < shortestDistance):
                shortestDistance = distance
                targetIndex = i
        #append closest node to result list and remove from working list
        newNodeList.append(workingNodeList[targetIndex])
        del workingNodeList[targetIndex]
	newIndex = newIndex+1

#=====================================================================


    print("Main: Initial totalTourWeight: ")
    print(totalTourWeight)

    finalTotalTourWeight = getTotalTourWeight(newNodeList)
    print("\nMain: finalTotalTourWeight: ")
    print(finalTotalTourWeight)
    print("\n")

    print("Input file: " + str(fileName))
    print("Saving Results.")
    saveResults(fileName, newNodeList, finalTotalTourWeight)

    print("\nDONE!\n")

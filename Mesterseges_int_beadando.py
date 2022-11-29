import random
import math
import time
import matplotlib.pyplot as plt
import numpy as np

def main():
    pauseArray=[]
    maxIterationsNumber,maxIterationTests_number,generationSeed,numWorks,machinesNum,pauseNum,pauseArray=readFile()
    fileOutput = open("output.txt", "w")
    print("Generated datas and logs can be found in output.txt")
    for i in range(len(generationSeed)):
        print("\n\n\n\n",i,". generation: \n\n\n")
        fileOutput.write("\n\n\n\n"+str(i)+". generation: \n\n\n")
        random.seed(int(generationSeed[i]))
        jobsArray = [[0 for x in range(int(machinesNum[i]))] for y in range(int(numWorks[i]))]
        jobsArray = generateRandomJobs(int(machinesNum[i]),int(numWorks[i]),fileOutput)
        startSearch(int(maxIterationsNumber[i]),int(maxIterationTests_number[i]),int(machinesNum[i]),int(numWorks[i]),pauseArray[i],int(pauseNum[i]),jobsArray,fileOutput)
    print("Done")
    
    fileOutput.close()
    
def readFile():
    fileInput=open("adatok.txt", "r")
    generationSeed=[]
    pauseArray=[]
    maxIterationsNumber=[]
    maxIterationTests_number=[]
    numWorks=[]
    machinesNum=[]
    pauseNum=[]
    
    fileInput.readline()
    inputData=fileInput.readline().replace('\n','').split(" ")
    generationSeed+=inputData
    fileInput.readline()
    inputData=fileInput.readline().replace('\n','').split(" ")
    maxIterationsNumber+=inputData
    fileInput.readline()
    inputData=fileInput.readline().replace('\n','').split(" ")
    maxIterationTests_number+=inputData
    fileInput.readline()
    inputData=fileInput.readline().replace('\n','').split(" ")
    numWorks+=inputData
    fileInput.readline()
    inputData=fileInput.readline().replace('\n','').split(" ")
    machinesNum+=inputData
    fileInput.readline()
    inputData=fileInput.readline().replace('\n','').split(" ")
    pauseNum+=inputData
    fileInput.readline()
    for i in range(len(pauseNum)):
        splitted=fileInput.readline().replace('\n','').split(" ")
        tempPauses = []
        for k in splitted:
            splitt_of_splitted = k.split("-")
            tempPauses.append(splitt_of_splitted)
        pauseArray.append(tempPauses)
    fileInput.close()
    return maxIterationsNumber,maxIterationTests_number,generationSeed,numWorks,machinesNum,pauseNum,pauseArray


def generateRandomJobs(machinesNum,numWorks,fileOutput):
    jobsArray = [[0 for x in range(machinesNum)] for y in range(numWorks)]
    for i in range (numWorks):
        fileOutput.write("J"+str(i)+"\t")
    fileOutput.write("\n")
    for macs in range(machinesNum):
        for jobs in range(numWorks):
            jobsArray[jobs][macs]=random.randint(1,10)
            fileOutput.write(str(jobsArray[jobs][macs]))
            fileOutput.write("\t")
        fileOutput.write("\n")
    return jobsArray

def startSearch(maxIterationsNumber,maxIterationTests_number,machinesNum,numWorks,pauseArray,pauseNum,jobsArray,fileOutput):
    plt.style.use('_mpl-gallery')
    fig, ax = plt.subplots()
    currentBestSearch = alltimeBest = ITERATIONS = 0
    bestSolution = []
    bestSolutionTemp = []
    base = []
    baseTemp = []
    
    for i in range(numWorks):
        base+=[i]

    
    fileOutput.write("Base lineup: "+printArray(base)+"\n")
    bestSolution = base.copy()

    
    
    for i in range(maxIterationsNumber):
        for p in range(maxIterationTests_number):
            baseTemp,ITERATIONS,currentBestSearch,alltimeBest,bestSolutionTemp=startTest(machinesNum,numWorks,jobsArray,currentBestSearch,alltimeBest,bestSolution,pauseArray,pauseNum,fileOutput,base,ITERATIONS,ax)
            base=baseTemp.copy()
            bestSolution=bestSolutionTemp.copy()

    
    fileOutput.write("\n\n\nThe best way: "+str(printArray(bestSolution))+"with time: "+str(alltimeBest))
    print("Best way: ",str(printArray(bestSolution)), "\nTime: ",alltimeBest)


    
    result,currentBestSearch,alltimeBest,bestSolution,time=simulation(machinesNum,numWorks,jobsArray,bestSolution,currentBestSearch,alltimeBest,bestSolution,pauseArray,pauseNum,1,ax)
    ax.set(xlim=(0, alltimeBest), xticks=np.arange(0, alltimeBest),
       ylim=(0, machinesNum), yticks=np.arange(0, machinesNum+1))
    plt.show()

    

def startTest(machinesNum,numWorks,jobsArray,currentBestSearch,alltimeBest,bestSolution,pauseArray,pauseNum,fileOutput,base,ITERATIONS,ax):
    data = []
    data = base.copy()
    baseTemp = base.copy()
    a = random.randint(0,numWorks-1)
    b = random.randint(0,numWorks-1)
    
    while a==b:
         a = random.randint(0,numWorks-1)
         b = random.randint(0,numWorks-1)
    temp=data[a]
    data[a]=data[b]
    data[b]=temp
    
    result,currentBestSearch,alltimeBest,bestSolution,time=simulation(machinesNum,numWorks,jobsArray,data,currentBestSearch,alltimeBest,bestSolution,pauseArray,pauseNum,0,ax)

    if result==1:
        baseTemp=data.copy()
        fileOutput.write("Found new best time: "+printArray(data)+" with "+str(currentBestSearch)+ "time\n")
    elif result==0:
        temp=pow(0.95,ITERATIONS)*100000
        if temp==0:
            fileOutput.write("New Worse base found and declined: "+printArray(data)+" with "+str(time)+" Chance: 0\n")
        else:
            if random.random()<math.exp((alltimeBest-time)/temp):
                fileOutput.write("New Worse base found and accepted: "+printArray(data)+" with "+str(time)+ "time. Chance: "+str(math.exp((alltimeBest-time)/temp))+"\n")
                baseTemp=data.copy()
                currentBestSearch=time
            else:
                fileOutput.write("New Worse base found and declined: "+printArray(data)+" with "+str(time)+" Chance: "+str(math.exp((alltimeBest-time)/temp))+"\n")
    return baseTemp,ITERATIONS+1,currentBestSearch,alltimeBest,bestSolution

def simulation(machinesNum,numWorks,jobsArray,jobsOrder,currentBestSearch,alltimeBest,bestSolution,pauseArray,pauseNum,mode,ax):
    startMachine = [[0 for x in range(int(numWorks))] for y in range(int(machinesNum))]
    endMachine = [[0 for x in range(int(numWorks))] for y in range(int(machinesNum))]

    for i in range(numWorks):
        for r in range(machinesNum):
            if i==0:
                if r==0:
                    startMachine[jobsOrder[i]][r]=0
                    for k in range(pauseNum):
                        if not currentWork_and_pauses(int(startMachine[jobsOrder[i]][r]),jobsArray[jobsOrder[i]][r],pauseArray,pauseNum,k):
                            startMachine[jobsOrder[i]][r]=int(pauseArray[k][1])
                        elif int(pauseArray[k][1])>int(startMachine[jobsOrder[i]][r])+int(jobsArray[jobsOrder[i]][r]):
                            break
                else:
                    startMachine[jobsOrder[i]][r]=endMachine[jobsOrder[i]][r-1]
                    for k in range(pauseNum):
                        if not currentWork_and_pauses(int(startMachine[jobsOrder[i]][r]),jobsArray[jobsOrder[i]][r],pauseArray,pauseNum,k):
                            startMachine[jobsOrder[i]][r]=int(pauseArray[k][1])
                        elif int(pauseArray[k][1])>int(startMachine[jobsOrder[i]][r])+int(jobsArray[jobsOrder[i]][r]):
                            break
            else:
                if r==0:
                    startMachine[jobsOrder[i]][r]=endMachine[jobsOrder[i-1]][r]
                    for k in range(pauseNum):
                        if not currentWork_and_pauses(int(startMachine[jobsOrder[i]][r]),jobsArray[jobsOrder[i]][r],pauseArray,pauseNum,k):
                            startMachine[jobsOrder[i]][r]=int(pauseArray[k][1])
                        elif int(pauseArray[k][1])>int(startMachine[jobsOrder[i]][r])+int(jobsArray[jobsOrder[i]][r]):
                            break
                else:
                    if endMachine[jobsOrder[i]][r-1] > endMachine[jobsOrder[i-1]][r]:
                        startMachine[jobsOrder[i]][r]=endMachine[jobsOrder[i]][r-1]
                        for k in range(pauseNum):
                            if not currentWork_and_pauses(int(startMachine[jobsOrder[i]][r]),jobsArray[jobsOrder[i]][r],pauseArray,pauseNum,k):
                                startMachine[jobsOrder[i]][r]=int(pauseArray[k][1])
                            elif int(pauseArray[k][1])>int(startMachine[jobsOrder[i]][r])+int(jobsArray[jobsOrder[i]][r]):
                                break
                    else:
                        startMachine[jobsOrder[i]][r]=endMachine[jobsOrder[i-1]][r]
                        for k in range(pauseNum):
                            if not currentWork_and_pauses(int(startMachine[jobsOrder[i]][r]),jobsArray[jobsOrder[i]][r],pauseArray,pauseNum,k):
                                startMachine[jobsOrder[i]][r]=int(pauseArray[k][1])
                            elif int(pauseArray[k][1])>int(startMachine[jobsOrder[i]][r])+int(jobsArray[jobsOrder[i]][r]):
                                break
            endMachine[jobsOrder[i]][r]=int(startMachine[jobsOrder[i]][r])+int(jobsArray[jobsOrder[i]][r])
            if mode:
                ax.bar(startMachine[jobsOrder[i]][r], 1, width=jobsArray[jobsOrder[i]][r],bottom=machinesNum-r-1, edgecolor="white", linewidth=0.7,align='edge',color=str((r%2)/2))

    time = endMachine[jobsOrder[numWorks-1]][numWorks-1]
    bestSolutionTemp = bestSolution.copy()
    
    if currentBestSearch == 0:
        currentBestSearch = time
        
    if alltimeBest == 0:
        alltimeBest = currentBestSearch
        
    if currentBestSearch > time:
        currentBestSearch = time
        if alltimeBest > currentBestSearch:
            alltimeBest = currentBestSearch
            bestSolutionTemp=jobsOrder.copy()
        return 1,currentBestSearch,alltimeBest,bestSolutionTemp,time

    if currentBestSearch == time:
        return 2,currentBestSearch,alltimeBest,bestSolutionTemp,time
    
    return 0,currentBestSearch,alltimeBest,bestSolutionTemp,time

def currentWork_and_pauses(time,workCurrent,pauseArray,pauseNum,i):
    if time>=int(pauseArray[i][0]) and time<=int(pauseArray[i][1]):
        return False
    if time+workCurrent>int(pauseArray[i][0]) and time+workCurrent<=int(pauseArray[i][1]):
        return False
    if time<=int(pauseArray[i][0]) and time+workCurrent>=int(pauseArray[i][1]):
        return False
    return True


def printArray(array):
    string=""
    j=0
    for i in array:
        string+="J"+str(array[j])+" "
        j+=1
    return string

if __name__ == "__main__":
    main()

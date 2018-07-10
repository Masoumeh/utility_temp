# inserting milestones for splitting texts into chunks of the same size

import re, os, shutil

splitter = "#META#Header#End#"
milestone = "Milestone300"

import math 
def roundup(x, par):
    newX = int(math.ceil(int(x) / float(par)) * par)
    return(newX)

def mechanical_chunking(file):
    
    fileName = dataDic[file][1].split("/")[-1]
    print("\n"+ fileName)
    #print(dataDic[file])
    #print(dataDic[file][3])

    targetSubfolder = targetFolder + dataDic[file][2] + file+"/"
    print(targetSubfolder)

    # Check if regeneration is requested
    # Only .mARkdown and .completed need to be regenerated; other texts do not
    if forceRegen == "y":
        if file.endswith((".mARkdown", ".completed", ".inProgress")):
            if os.path.exists(targetSubfolder):
                shutil.rmtree(targetSubfolder)
                print(dataDic[file])
                dataDic[file][3] = "0"
                print(dataDic[file])
                
                print("\tData for %s must be regenerated..." % fileName)
                input()
    elif forceRegen == "n":
        pass
    else:
        input("Unrecognized `forceRegen` value! Use `y` or `n`...")

    # run generation
    if dataDic[file][3] == "0":
        if not os.path.exists(targetSubfolder):
            os.makedirs(targetSubfolder)
        # process
##        print("tada")
##        input(dataDic[file][1])
        with open(dataDic[file][1], "r", encoding="utf8") as f1:
            data = f1.read()
            data = data.split(splitter)[1]
            data = data.split(milestone)

            print("\t%d files will be created..." % len(data))

            counter = 0
            for d in data:
                counter += 1
                d = "... %s ..." % d

                with open(targetSubfolder+"%s_%08d" % (milestone, counter), "w", encoding="utf8") as ft:
                    ft.write(d)

        # update the dic value
        dataDic[file][3] = "1"
        count = 1
    else:
        count = 0
        
    return(count)

def loadIndex():
    dataList = []
    dataDic  = {}
    with open("i.mech_index.txt", "r", encoding="utf8") as f1:
        data = f1.read().split("\n")
        dataList = data
        for d in data:
            d = d.split("\t")
            dataDic[d[0]] = d
    return(dataList, dataDic)       

# process all texts in OpenITI
def processAll(folder):
    dic1 = {}

    print("Files total: %d" % len(dataList))                
    print()
    print("Generating mechanical corpus...")
    print()

    count = 0
    for d in dataList:
        d = d.split("\t")[0]
        #print(d)
        if count % 100 == 0:
            print()
            print("============="*2)
            print("Processed: %d" % count)
            print("============="*2)
            print()
        count += mechanical_chunking(d)       
        if count == 5000:
            break

    # update dataList
    newDataList = []
    for d in dataList:
        dKey = d.split("\t")[0]
        dNew = "\t".join(dataDic[dKey])
        newDataList.append(dNew)
        #input(dNew)

    with open("i.mech_index.txt", "w", encoding="utf8") as f9:
        f9.write("\n".join(newDataList))
        

targetFolder = "/Users/romanov/Documents/a.UCA_Centennial/OpenITI/"
mainFolder   = "/Users/romanov/Documents/a.UCA_Centennial/OpenITI/"

forceRegen = "n" # "y" to force regeneration of .completed and .mARkdown

import generate_imech_index

dataList, dataDic = loadIndex() 

processAll(mainFolder)

print("Done!")

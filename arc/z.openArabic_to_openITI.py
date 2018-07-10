# inserting milestones for splitting texts into chunks of the same size

import re

splitter = "#META#Header#End#"

def toOpenITI(file):
    fileName = file.split("/")[-1]
    #print(fileName)
    
    with open(file, "r", encoding="utf8") as f1:
        text = f1.read()

        # test if it is already OpenITI
        if text.startswith("######OpenITI#"):
            #print("\tthe file is already in `OpenITI mARkdown`")
            pass
        else:
            # run find/replace
            text = re.sub("\n#####ARABICA#SUBJECT(#XXX)?#", "\n#META#Header#End#", text)
            text = re.sub("#####FILENAME#\w+", "#META#Header#End#\n", text)
            text = re.sub("^#####ARABICA#SUBJECT#", "######OpenITI#", text)
            text = re.sub("######## BEGofRECORD #########+ ?\n", "", text)

            text = re.sub(r"\n#(NewRec|OldRec|000000)#", r"\n#META#", text)

            print(fileName)
            print("\tthe file is converted into `OpenITI mARkdown`")

        #text = re.sub("#####FILENAME#\w+", "#META#Header#End#\n", text)

        

        # save
        with open(file, "w", encoding="utf8") as f9:
            f9.write(text)
                

#path = "/Users/romanov/Documents/a.UCA_Centennial/OpenITI/0750AH/data/0748Dhahabi/0748Dhahabi.TarikhIslam/"
#toOpenITI(path+"0748Dhahabi.TarikhIslam.Shamela0035100-ara1.mARkdown")

# process all texts in OpenITI

import os
def processAll(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if re.search("^\d{4}\w+\.\w+\.\w+-\w\w\w\d(\.\w+)?$", file):
                toOpenITI(os.path.join(root,file))
    
processAll(".")


print("Done!")

# inserting milestones for splitting texts into chunks of the same size

import re

splitter = "#META#Header#End#"
arRa     = re.compile("^[ذ١٢٣٤٥٦٧٨٩٠ّـضصثقفغعهخحجدًٌَُلإإشسيبلاتنمكطٍِلأأـئءؤرلاىةوزظْلآآ]+$")

def milestones(file, length):
    fileName = file.split("/")[-1]
    print(fileName)
    
    with open(file, "r", encoding="utf8") as f1:
        data = f1.read()

        # splitter test
        if splitter in data:
            #pass
            # MilestonesTEST
            ms = re.findall("Milestone%d" % length, data)
            if len(ms) > 0:
                print("\tthe text already have %d milestones of this length" % len(ms))
                pass
            else:
                # insert Milestones
                newData = []
                head = data.split(splitter)[0]
                text = data.split(splitter)[1]
                
                data = re.findall(r"\w+|\W+", text)

                tokenCount = 0
                milestoneC = 0

                newData = []
                
                for d in data:
                    if arRa.search(d):
                        tokenCount += 1
                        newData.append(d)
                        
                    else:
                        newData.append(d)

                    if tokenCount == length:
                        milestoneC += 1
                        milestone = " Milestone%d" % (length)
                        newData.append(milestone)
                        tokenCount = 0

                msText = "".join(newData)
                #msText = re.sub(" +", " ", msText)

                test = re.sub(" Milestone\d+", "", msText)
                #test = re.sub(" +", " ", test)

                if test == text:
                    print("\t\tThe file has not been damaged!")
                    # MilestonesTEST
                    ms = re.findall("Milestone%d" % length, msText)
                    print("\t\t%d milestones (%d words)" % (len(ms), length))
                else:
                    input("\t\tSomething got messed up...")

                msText = head + splitter + msText

                with open(file, "w", encoding="utf8") as f9:
                    f9.write(msText)

        else:
            print("The file is missing the splitter!")
            print(file)

# process all texts in OpenITI
import os
def processAll(folder):
    exclude = (["OpenITI.github.io", "Annotation", "_maintenance", "i.mech"])
    for root, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d not in exclude]   
        for file in files:
            if re.search("^\d{4}\w+\.\w+\.\w+-ara\d(\.\w+)?$", file):
                #print(os.path.join(root,file).replace("\\", "/"))
                milestones(os.path.join(root,file), 300)
                #input()
    
processAll(".")


print("Done!")

import re, os, shutil, textwrap

import zfunc

def removeFilesByPattern(folder):

    data = []
    counter = 0

    exclude = (["OpenITI.github.io", "Annotation", "_maintenance", "i.mech"])
    for root, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d not in exclude]   

        for file in files:
            if re.search("\.metadata\.yml$", file):
                pathFull = os.path.join(root, file)

                os.remove(pathFull)

                #print(pathFull)
                #input()

removeFilesByPattern("/Users/romanov/Documents/a.UCA_Centennial/OpenITI/")

print("Done!")

import time, re, os, shutil, textwrap

import betaCode
import zfunc

start = time.time()

def collectMetadata(folder):
    
    counter = 0

    exclude = (["OpenITI.github.io", "Annotation", "maintenance", "i.mech"])
    for root, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d not in exclude]   
        for file in files:
            if re.search("^\d{4}[A-Za-z]+\.[A-Za-z]+\.\w+-(ara|per)\d\.(mARkdown|completed|inProgress)$", file):

                counter += 1
                print(file)


    print()
    print(counter)
    print()




collectMetadata("/Users/romanov/Documents/a.UCA_Centennial/OpenITI/")

end = time.time()
print("Processing time: {0:.2f} sec".format(end - start))
print("Tada!")

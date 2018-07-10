# Functions to remove unnecessary characters or parts/text from OpenITI texts.

import re
import os
import zfunc


def clean_file(path_full, to_remove, to_replace):

    splitter = "#META#Header#End#"
    fileName = path_full.split("/")[-1]
    print("\npf: " + path_full)
    # fileID = re.sub("\d{4}\w+\.\w+\.", "", fileName)

    # targetPath = targetFolder + fileName

    with open(path_full, "r+", encoding="utf8") as f1:
        data = f1.read()
        data_header = data.split(splitter)[0]
        data_text = data.split(splitter)[1]
        data_text = re.sub(to_remove, to_replace, data_text)
        data = "".join([data_header, splitter, data_text])
        f1.seek(0)
        f1.write(data)
        f1.truncate()


def processAll(folder, to_remove, to_replace):
    dic1 = {}

    print()
    print("Generating mechanical passim_new corpus...")
    print()

    count = 1

    for root, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d not in zfunc.exclude]

        for file in files:
            # print("file: %s" % file)
            if re.search("^\d{4}\w+\.\w+\.\w+-\w{4}(\.(mARkdown|inProgress|completed))?$", file):
                pathFull = os.path.join(root, file)
                print("pathfile: %s" % pathFull)

                if "" in pathFull:
                    clean_file(pathFull, to_remove, to_replace)
                    # return




mainFolder = "/media/rostam/Seagate Backup Plus Drive/OpenITI/"
# targetFolder = "/home/rostam/projs/KITAB/OpenITI/Clean/"

remove_phrase = "\n#\n"
replace_phrase = "\n"
processAll(mainFolder, remove_phrase, replace_phrase)

print("Done!")
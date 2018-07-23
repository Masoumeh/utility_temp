# Functions to remove unnecessary characters or parts/text from OpenITI texts.

import re
import os
import zfunc


def clean_file(path_full, to_remove, to_replace):
    splitter = "#META#Header#End#"
    print("\npf: " + path_full)

    with open(path_full, "r+", encoding="utf8") as f1:
        data = f1.read()
        data_header = data.split(splitter)[0]
        data_text = data.split(splitter)[1]
        data_text = re.sub(to_remove, to_replace, data_text)
        data = "".join([data_header, splitter, data_text])
        f1.seek(0)
        f1.write(data)
        f1.truncate()


def process_all(folder, to_remove, to_replace):

    print()
    print("removing %s from OpeITI corpus..." % to_remove)
    print()

    for root, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d not in zfunc.exclude]

        for file in files:
            # print("file: %s" % file)
            if re.search("^\d{4}\w+\.\w+\.\w+-\w{4}(\.(mARkdown|inProgress|completed))?$", file):
                path_full = os.path.join(root, file)
                print("pathfile: %s" % path_full)

                if "" in path_full:
                    clean_file(path_full, to_remove, to_replace)
                    # return


main_folder = "/media/rostam/Seagate Backup Plus Drive/OpenITI/"
# targetFolder = "/home/rostam/projs/KITAB/OpenITI/Clean/"

remove_phrase = "\n#\n"
replace_phrase = "\n"
process_all(main_folder, remove_phrase, replace_phrase)

print("Done!")

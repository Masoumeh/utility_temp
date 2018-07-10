# Moves all ara1 file from all directories into a single directory

import os
import re
import shutil
import sys


def move_ara_files(source_dir, dest_dir):
    for root, dirs, files in os.walk(source_dir):
        # print("root: ",root)
        dirs[:] = [d for d in dirs]

        for file in files:
            if re.search("^\d{4}\w+\.\w+\.\w+-ara_old\d$", file):
                shutil.copy(os.path.join(root, file), dest_dir)


if __name__ == '__main__':

    source = input("Enter the source directory: ")
    target = input("Enter the target directory: ")

    if len(sys.argv) > 0:
        if not os.path.exists(source):
            print("source directory doesn't exists!")
        elif not os.path.exists(target):
            os.makedirs(target) if target else print("please enter a target path")
        else:
            move_ara_files(source, target)
    else:
        print("give the path to the script...!")
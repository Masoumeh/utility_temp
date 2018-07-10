# Preparing passim instantiation of OpenITI based on the logical unit ids.

import math
import os
import re
from ara import ara_manipulation
import json

import zfunc

def mark_replcements(d):
    d = d.replace("\n~~", " ")
    d = d.replace("#", "(@@)")
    d = d.replace("\n", "(@)")
    d = re.sub(" +", " ", d)
    return d


def full_book_chunking(path_full, target_folder):

    splitter = "#META#Header#End#"
    # log_units_regex = "\n#\d+-\d+"
    ar_ra = re.compile("^[ذ١٢٣٤٥٦٧٨٩٠ّـضصثقفغعهخحجدًٌَُلإإشسيبلاتنمكطٍِلأأـئءؤرلاىةوزظْلآآ]+$")
    file_name = path_full.split("/")[-1]
    # print("\n" + file_name)
    file_id = re.sub("\d{4}\w+\.\w+\.", "", file_name)

    target_path = target_folder + file_id

    if os.path.exists(target_path):
        count = 0
    else:
        with open(path_full, "r", encoding="utf8") as f1:
            data = f1.read()
            text = data.split(splitter)[1].strip()

            # JSON record structure for chunks.
            # Number of chunks to be written in each file. When it reaches thresh (1000), resets and no
            # more records will be added to that file.
            rec = '{"id":"%s", "series":"%s", "text": "%s"}'#, "unit_ids": [%s] }'
            create_chunks(ar_ra, file_id, rec, target_path, text)

        # count = 1

    # return count


def create_chunks(ar_ra, file_id, rec, target_path, data):

    # Array of json records (chunks) to be written in the files
    # cex = []
    text = mark_replcements(data)
    clean_text = ara_manipulation.textCleaner(text)  # .strip()
    # write text to file
    write_chunk(file_id, clean_text, rec, target_path)


def ar_token_cnt(ar_ra, text):
    return sum(ar_ra.search(t) is not None for t in re.findall(r"\w+|\W+", text))


def write_chunk(file_id, text, rec, target_path):
    # cex = []
    chunk_id = file_id + ".full-book"
    chunk = rec % (chunk_id, file_id, text)#, ids_in_chunk)
    # cex.append(chunk)
    with open(target_path, "w", encoding="utf8") as ft:
          ft.write(chunk)
    # cex = []
    # return cex


# process all texts in OpenITI
def process_all(input_folder, target_folder):

    print("\nGenerating logical passim corpus with logical ids included ...\n")

    for root, dirs, files in os.walk(input_folder):
        dirs[:] = [d for d in dirs if d not in zfunc.exclude]

        for file in files:
            # print("file: %s" % file)
            if re.search("^\d{4}\w+\.\w+\.\w+-\w{4}(\.(mARkdown|inProgress|completed))?$", file):
                path_full = os.path.join(root, file)
                f_name = path_full.split("/")[-1]
                print(f_name)

                if "" in path_full:
                    full_book_chunking(path_full, target_folder)


main = "/home/rostam/projs/KITAB/OpenITI/"
target = "/home/rostam/projs/KITAB/OpenITI/i.passim_log_Temp/"

process_all(main, target)

print("Done!")

'''
inserting logical unit ids for splitting texts into logical chunks
The ids are added before a logical unit (or paragraph) starts with the following pattern, including two numbers:
    "#\d[number of the words in text]-\d"
where the numbers are pointers to the sequential position of the first and last tokens in this unit respectively.
It will for the logical units as below:
#000007-89# الحمد لله الذي شرف نوع الإنسان ، بالأصغرين : القلب واللسان ، وفضله على
...
'''
import re
import os


splitter = "#META#Header#End#"
arRa = re.compile("^[ذ١٢٣٤٥٦٧٨٩٠ّـضصثقفغعهخحجدًٌَُلإإشسيبلاتنمكطٍِلأأـئءؤرلاىةوزظْلآآ]+$")


def logical_units(file):
    para_splitter = "\n#+"
    fileName = file.split("/")[-1]

    with open(file, "r", encoding="utf8") as f1:
        book = f1.read()

        # splitter test
        if splitter in book:
            # pass
            # logical units
            log_ids = re.findall("\n#\d+#", book)
            if len(log_ids) > 0:
                print("\tthe text already have %d logical units of this length" % len(log_ids))
                pass
            else:
                # insert logical unit ids
                newData = []
                head = book.split(splitter)[0]
                text = book.split(splitter)[1]#.strip()
                tokenCount = 0

                paras = re.split(para_splitter, text)
                paras_len = len(paras)
                data = re.findall(r"\w+|\W+", text)
                word_len = len(str(len(data)))
                data_len = len(data)

                for p in paras:
                    p_toks = re.findall(r"\w+|\W+", p)
                    # p_toks_len = 0
                    p_toks_len = sum(arRa.search(t) != None for t in p_toks)
                    if p_toks_len > 0:
                        tmp_log_id = "".join(["\n#", str(tokenCount + 1).zfill(word_len), "-",
                                          str(tokenCount + p_toks_len), "#"])
                        tokenCount += p_toks_len
                    # insert it at the beggining of the tokens array in this paragraph
                        p_toks.insert(0, tmp_log_id)
                        newData.extend(p_toks)
                    else:
                        newData.extend(["\n#"] + p_toks)

                msText = "".join(newData)
                msText = head + splitter + "\n" + msText

                with open(file + "_logical2", "w", encoding="utf8") as f9:
                    f9.write(msText)

        else:
            print("The file is missing the splitter!")
            print(file)


# process all texts in OpenITI


def processAll(folder):
    exclude = (["OpenITI.github.io", "Annotation", "_maintenance", "i.mech"])
    for root, dirs, files in os.walk(folder):
        # print("root: ",root)
        dirs[:] = [d for d in dirs if d not in exclude]
        # print("dir: ",dirs)
        for file in files:
            if re.search("^\d{4}\w+\.\w+\.\w+-ara\d$", file):
                logical_units(os.path.join(root, file))
                # return
                # input()

# /media/rostam/Seagate Backup Plus Drive
processAll("/home/rostam/projs/KITAB/OpenITI")

print("Done!")

# inserting logical unit ids for splitting texts into logical chunks

import re
import os


splitter = "#META#Header#End#"
arRa = re.compile("^[ذ١٢٣٤٥٦٧٨٩٠ّـضصثقفغعهخحجدًٌَُلإإشسيبلاتنمكطٍِلأأـئءؤرلاىةوزظْلآآ]+$")


def logical_units(file):
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
                text = book.split(splitter)[1]
                tokenCount = 0

                data = re.findall(r"\w+|\W+", text)
                word_len = len(str(len(data)))
                data_len = len(data)

                for i in range(0, data_len):
                    if "\n#" in data[i]:
                        if "Page" in data[i + 1]:
                            newData.append(data[i])
                        else:
                            last = data[i].rfind("#")
                            tokenCnt_str = str(tokenCount + 1)
                            if len(tokenCnt_str) < word_len:
                                tmp_cnt = tokenCnt_str.zfill(word_len)
                            else:
                                tmp_cnt = tokenCnt_str
                            tmp = data[i][:last] + "#" + tmp_cnt + data[i][last:]
                            newData.append(tmp)

                    elif arRa.search(data[i]):
                        tokenCount += 1
                        newData.append(data[i])
                    else:
                        newData.append(data[i])

                msText = "".join(newData)
                msText = head + splitter + msText

                with open(file + "_logical", "w", encoding="utf8") as f9:
                    f9.write(msText)

        else:
            print("The file is missing the splitter!")
            print(file)


# process all texts in OpenITI


def process_all(folder):
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
# process_all("/home/rostam/projs/KITAB/OpenITI")

# print("Done!")

# inserting logical unit ids for splitting texts into logical chunks

import re
import os


splitter = "#META#Header#End#"
ar_ra = re.compile("^[ذ١٢٣٤٥٦٧٨٩٠ّـضصثقفغعهخحجدًٌَُلإإشسيبلاتنمكطٍِلأأـئءؤرلاىةوزظْلآآ]+$")


def logical_units(file):
    log_id_splitter = "(#\d+#)"
    log_id_pattern = re.compile("#\d+#")

    with open(file, "r", encoding="utf8") as f1:
        book = f1.read()

        # splitter test
        if splitter in book:
            # pass
            # logical units
            log_ids = re.findall(r"\n#\d+-\d+#", book)
            if len(log_ids) > 0:
                print("\tthe text already have %d logical units of this length" % len(log_ids))
                pass
            else:
                # insert logical unit ids
                new_data = []
                head = book.split(splitter)[0]
                text = book.split(splitter)[1]

                data = re.split(log_id_splitter, text)
                data_len = len(data)

                i = 0
                while i < data_len - 2:
                    if log_id_pattern.search(data[i]) is not None:
                        curr_id = re.findall(r"\d+", data[i])
                        nxt_id = int(re.findall(r"\d+", data[i + 2])[-1])
                        print("cur, nxt: ", curr_id, " ", curr_id[-1], " ", nxt_id)
                        if nxt_id != int(curr_id[-1]):
                            new_id = curr_id[-1] + "-" + str(nxt_id - 1)
                            new_log_id = "".join(["#", new_id, "#"])
                            new_data.extend(new_log_id)
                        else:
                            new_data.extend(data[i])
                    else:
                        new_data.extend(data[i])
                    i += 1

                if i == data_len - 2:
                    # log_id_pattern.search(data[i]) != None:
                    curr_id = re.findall(r"\d+", data[i])
                    nxt_toks = re.findall(r"\w+|\W+", data[i + 1])
                    nxt_toks_len = sum(ar_ra.search(t) is not None for t in nxt_toks)
                    print("len: ", nxt_toks_len)
                    if nxt_toks_len > 0:
                        new_id = curr_id[-1] + "-" + str(int(curr_id[-1]) + nxt_toks_len - 1)
                        new_log_id = "".join(["#", new_id, "#"])
                        new_data.extend([new_log_id, data[i + 1]])
                    else:
                        new_data.extend(data[i + 1])
                log_text = "".join(new_data)
                log_text = head + splitter + log_text

                with open(file + "2", "w", encoding="utf8") as f:
                    f.write(log_text)

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
            if re.search("^\d{4}\w+\.\w+\.\w+-ara\d_logical$", file):
                logical_units(os.path.join(root, file))
                # return
                # input()

# /media/rostam/Seagate Backup Plus Drive
# process_all("/home/rostam/projs/KITAB/test")

# print("Done!")

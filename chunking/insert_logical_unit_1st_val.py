# inserting logical unit ids for splitting texts into logical chunks

import re
import os

splitter = "#META#Header#End#"


def logical_units(file):
    ar_ra = re.compile("^[ذ١٢٣٤٥٦٧٨٩٠ّـضصثقفغعهخحجدًٌَُلإإشسيبلاتنمكطٍِلأأـئءؤرلاىةوزظْلآآ]+$")

    with open(file, "r", encoding="utf8") as f1:
        book = f1.read()

        # splitter test
        if splitter in book:
            # logical units
            log_ids = re.findall("\n#\d+#", book)
            if len(log_ids) > 0:
                print("\tthe text already have %d logical units of this length" % len(log_ids))
                pass
            else:
                # insert logical unit ids
                new_data = []
                head = book.split(splitter)[0]
                text = book.split(splitter)[1]
                token_count = 0

                data = re.findall(r"\w+|\W+", text)
                word_len = len(str(len(data)))
                data_len = len(data)

                for i in range(0, data_len):
                    if "\n#" in data[i]:
                        if "Page" in data[i + 1]:# or ar_token_cnt(ar_ra, data[i + 1]) <= 0:
                            new_data.append(data[i])
                        else:
                            last = data[i].rfind("#")
                            token_cnt_str = str(token_count + 1)
                            if len(token_cnt_str) < word_len:
                                tmp_cnt = token_cnt_str.zfill(word_len)
                            else:
                                tmp_cnt = token_cnt_str
                            tmp = data[i][:last] + "#" + tmp_cnt + data[i][last:]
                            new_data.append(tmp)

                    elif ar_token_cnt(ar_ra, data[i]):
                        token_count += 1
                        new_data.append(data[i])
                    else:
                        new_data.append(data[i])

                log_text = "".join(new_data)
                log_text = head + splitter + log_text

                with open(file + "_logical", "w", encoding="utf8") as f:
                    f.write(log_text)

        else:
            print("The file is missing the splitter!")
            print(file)


def ar_token_cnt(ar_ra, text):
    return sum(ar_ra.search(t) is not None for t in re.findall(r"\w+|\W+", text))


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
# process_all("/home/rostam/projs/KITAB/test")

# print("Done!")

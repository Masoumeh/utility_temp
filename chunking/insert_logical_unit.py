"""
inserting logical unit ids for splitting texts into logical chunks
The ids are added before a logical unit (or paragraph) starts with the following regex pattern, including two numbers:
    "#\d[number of the words in text]-\d"
where the numbers are pointers to the sequential position of the first and last tokens in this unit respectively.
It will for the logical units as below:
#000007-18# الحمد لله الذي شرف نوع الإنسان ، بالأصغرين : القلب واللسان ، وفضله على
"""
import re
import os

splitter = "#META#Header#End#"
ar_ra = re.compile("^[ذ١٢٣٤٥٦٧٨٩٠ّـضصثقفغعهخحجدًٌَُلإإشسيبلاتنمكطٍِلأأـئءؤرلاىةوزظْلآآ]+$")


def logical_units(file):
    para_splitter = "\n#"

    with open(file, "r", encoding="utf8") as f1:
        book = f1.read()

        # splitter/header test
        if splitter in book:
            # pass
            # logical units
            log_ids = re.findall("\n#\d+#", book)
            if len(log_ids) > 0:
                print("\tthe text already have %d logical units of this length" % len(log_ids))
                pass
            else:
                new_data = []
                # split the header and body of the text. We will nedd the body which is stored in the text variable.
                head = book.split(splitter)[0]
                text = book.split(splitter)[1]  # .strip()  # we don't split to save the orignal text as it is
                tokenCount = 0

                # split the text into paragraphs by "\n#"
                paras = re.split(para_splitter, text)
                data = re.findall(r"\w+|\W+", text)
                word_len = len(str(len(data)))

                # insert logical unit ids
                for i in range(0, len(paras)):
                    # find all tokens in this paragraph
                    p_toks = re.findall(r"\w+|\W+", paras[i])
                    # count the number of tokens which include Arabic letters or numbers
                    p_toks_len = sum(ar_ra.search(t) is not None for t in p_toks)
                    # if the paragraph has Arabic characters, proceed with creating and adding logical id to this paraf
                    if p_toks_len > 0:
                        # the id has two part: "position of the first token of the paragraph (in the entire text)-
                        # position of the last token of the paragraph (in the entire text)"
                        # we also add # to the end of the id string, e.g. "#0000012-98#". Then we add "\n#" before this
                        # string to re-attach what we have removed from this paragraph while splitting. The new
                        tmp_log_id = "".join(["\n#", str(tokenCount + 1).zfill(word_len), "-",
                                              str(tokenCount + p_toks_len), "#"])
                        tokenCount += p_toks_len
                        # insert the generated id string at the beginning of the tokens array in this paragraph
                        p_toks.insert(0, tmp_log_id)
                        # append the new paragraphs (which starts with "\n#id1-id2#") to the new
                        new_data.extend(p_toks)
                    # if the paragraph doesn't have any Arabic charachter, we just keep it without producing any log id
                    else:
                        # if this paragraph is the first one in "paras", it shouldn't add any "\n#". The reason:
                        # the text either starts with "\n#" which in that case the fist "p" in "paras" will be an empty
                        # str, '', which doesn't need and extra "\n#". Or the text starts with sth other than "\n#" that
                        # means nothing has been cut from the original paragraph and there is no need to add "\n#" at
                        # at the beginning of the paragraph "p". Thos case only happens in the first paragraph. That's
                        # why we add this if statement to check the index of "p".
                        if i == 0:
                            new_data.extend(p_toks)
                        # For other paragraphs ("p"), we add "\n#" since this is a splitter and had been cut from the
                        # start of the paragraph.
                        else:
                            new_data.extend(["\n#"] + p_toks)

                ms_text = "".join(new_data)
                ms_text = head + splitter + "\n" + ms_text

                with open(file + "_logical_new", "w", encoding="utf8") as f:
                    f.write(ms_text)

        else:
            print("The file is missing the splitter!")
            print(file)


# process all texts in OpenITI
def process_all(folder):
    exclude = (["OpenITI.github.io", "Annotation", "_maintenance", "i.mech"])
    for root, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d not in exclude]
        for file in files:
            # process the files that end with "ara1"!
            if re.search("^\d{4}\w+\.\w+\.\w+-ara\d$", file):
                logical_units(os.path.join(root, file))


process_all("/home/rostam/projs/KITAB/Sira/Ibn Ishaq by Source/OpenITI_sources/")

print("Done!")

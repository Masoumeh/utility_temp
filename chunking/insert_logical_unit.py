# Preparing passim instantiation of OpenITI based on the logical unit ids.
import csv
import os
import re
import zfunc
from ara import ara_manipulation


def mark_replcements(d):
    d = d.replace("\n~~", " ")
    d = d.replace("#", "(@@)")
    d = d.replace("\n", "(@)")
    d = re.sub(" +", " ", d)
    return d


def logical_chunking(path_full, thresh, min_len, max_len, target_folder):

    splitter = "#META#Header#End#"
    log_units_regex = "#\d+-\d+"
    ar_ra = re.compile("^[ذ١٢٣٤٥٦٧٨٩٠ّـضصثقفغعهخحجدًٌَُلإإشسيبلاتنمكطٍِلأأـئءؤرلاىةوزظْلآآ]+$")
    file_name = path_full.split("/")[-1]
    # print("\n" + file_name)
    file_id = re.sub("\d{4}\w+\.\w+\.", "", file_name)

    target_path = target_folder + file_id

    if os.path.exists(target_path + "-%05d" % thresh):
        count = 0
    else:
        with open(path_full, "r", encoding="utf8") as f1:
            data = f1.read()
            data = data.split(splitter)[1].strip()
            logical_units = re.split(log_units_regex, data)
            logical_ids = re.findall(log_units_regex, data)

            # JSON record structure for chunks.
            # Number of chunks to be written in each file. When it reaches thresh (1000), resets and no
            # more records will be added to that file.
            rec = '{"id":"%s", "series":"%s", "text": "%s", "unit_ids": %s }'

            # remove all logical units that don't have arabic tokens
            logical_units = [l for l in logical_units if
                             ar_token_cnt(ar_ra, l)]
            units_cnt = len(logical_units)
            # join units that happen in two pages
            tmp_joins = join_units_in_pages(units_cnt, logical_ids, logical_units)
            units_joined = tmp_joins[0]
            unit_ids_joined = tmp_joins[1]

            # find the token length for units longer that 1000
            max_tok_nrs = get_units_len(units_joined, max_len)

            units_cnt = len(units_joined)
            # create logical chunks and write them to files in the given target path
            create_chunks(ar_ra, file_id, max_len, min_len, rec, target_path, thresh, unit_ids_joined, units_cnt,
                          units_joined)

        count = 1

    return count, max_tok_nrs


def create_chunks(ar_ra, file_id, max_len, min_len, rec, target_path, thresh, unit_ids_joined, units_cnt, units_joined):
    i = 0
    counter = 0
    # Array of json records (chunks) to be written in the files
    cex = []
    unit_ids_in_chunk = []
    prev_ids_in_chunk = []
    prev_text = ""
    # print("ids: ", unit_ids_joined)
    # print(len(unit_ids_joined), " len units: ", len(units_joined))
    while i < units_cnt:
        d = mark_replcements(units_joined[i])  # .strip()
        d_tokens = re.findall(r"\w+|\W+", d)
        d_tokens_len = sum(ar_ra.search(t) is not None for t in d_tokens)
        d_tokens_total_len = d_tokens_len
        text = ara_manipulation.textCleaner(d)  # .strip()
        unit_ids_in_chunk.append(unit_ids_joined[i])
        i += 1
        while d_tokens_len < min_len and i < units_cnt:
            d = mark_replcements(units_joined[i])  # .strip()
            d_tokens_len = ar_token_cnt(ar_ra, text) + ar_token_cnt(ar_ra, d)
            d_tokens_total_len += d_tokens_len
            unit_ids_in_chunk.append(unit_ids_joined[i])
            text += ara_manipulation.textCleaner(d)  # .strip()
            i += 1

        while d_tokens_len < max_len and i < units_cnt:
            d = mark_replcements(units_joined[i])  # .strip()
            d_tokens_len = ar_token_cnt(ar_ra, text) + ar_token_cnt(ar_ra, d)
            d_tokens_total_len += d_tokens_len
            unit_ids_in_chunk.append(unit_ids_joined[i])
            text += ara_manipulation.textCleaner(d)  # .strip()
            i += 1

        if i >= units_cnt:
            # if d_tokens_total_len > min_len:
            if prev_text != "":
                if d_tokens_total_len > min_len:
                    # write prev_tex to file
                    cex = write_chunk(cex, counter, file_id, prev_text, prev_ids_in_chunk, rec, target_path, thresh)
                    # cex = write_chunk(cex, counter, file_id, prev_text, rec, target_path, thresh)

                    counter += 1
                    # write text to file
                    cex = write_chunk(cex, counter, file_id, text, unit_ids_in_chunk, rec, target_path, thresh)
                else:
                    cex = write_chunk(cex, counter, file_id, prev_text + text, prev_ids_in_chunk + unit_ids_in_chunk,
                                      rec, target_path, thresh)
            else:
                cex = write_chunk(cex, counter, file_id, text, unit_ids_in_chunk, rec, target_path, thresh)

        elif counter >= 1:
            # if i >= units_cnt - 1:
                if d_tokens_total_len > min_len:
                    # write prev_tex to file
                    cex = write_chunk(cex, counter, file_id, prev_text, prev_ids_in_chunk, rec, target_path, thresh)
                    # cex = write_chunk(cex, counter, file_id, prev_text, rec, target_path, thresh)

                    counter += 1
                    # write text to file
                    cex = write_chunk(cex, counter, file_id, text, unit_ids_in_chunk, rec, target_path, thresh)
                    # cex = write_chunk(cex, counter, file_id, text, rec, target_path, thresh)

                    # print(cex)
                    # ID = file_id + ".log%d" % counter
                    # chunk = rec % (ID, file_id, text)#, unit_ids_in_chunk)
                    # cex.append(chunk)
                    # if counter % thresh == 0:
                    #     with open(target_path + "%05d" % counter, "w", encoding="utf8") as ft:
                    #         ft.write("\n".join(cex))
                    #     cex = []
                else:
                    cex = write_chunk(cex, counter, file_id, prev_text + text, prev_ids_in_chunk + unit_ids_in_chunk,
                                      rec, target_path, thresh)
                    # cex = write_chunk(cex, counter, file_id, prev_text + text,
                    #                   rec, target_path, thresh)

                    # ID = file_id + ".log%d" % counter
                    # chunk = rec % (ID, file_id, prev_text + text)#, prev_ids_in_chunk + unit_ids_in_chunk)
                    # cex.append(chunk)
                    # if counter % thresh == 0:
                    #     with open(target_path + "%05d" % counter, "w", encoding="utf8") as ft:
                    #         ft.write("\n".join(cex))
                    #     cex = []
            # else:
            #     cex = write_chunk(cex, counter, file_id, prev_text, prev_ids_in_chunk, rec, target_path, thresh)
                # cex = write_chunk(cex, counter, file_id, prev_text, rec, target_path, thresh)

                # ID = file_id + ".log%d" % counter
                # chunk = rec % (ID, file_id, prev_text)#, prev_ids_in_chunk)
                # cex.append(chunk)
                # if counter % thresh == 0:
                #     with open(target_path + "%05d" % counter, "w", encoding="utf8") as ft:
                #         ft.write("\n".join(cex))
                #     cex = []

        counter += 1
        prev_text = text
        prev_ids_in_chunk = unit_ids_in_chunk
        unit_ids_in_chunk = []
    counterFinal = zfunc.roundup(counter, thresh)
    print(target_path)
    with open(target_path + "%05d" % counterFinal, "w", encoding="utf8") as ft:
        ft.write("\n".join(cex))


def ar_token_cnt(ar_ra, text):
    return sum(ar_ra.search(t) is not None for t in re.findall(r"\w+|\W+", text))


def join_units_in_pages(log_units_len, ids, units):
    units_joined = []
    unit_ids_joined = []
    i = 0
    while i < log_units_len - 1:
        toks = re.findall(r"\w+|\W+", units[i].strip())
        tmp_unit = []
        tmp_ids = []
        page_indices = [i for i, t in enumerate(toks) if 'Page' in t]
        page_indices_continues = [i for i in page_indices if '#' not in toks[i - 1]]
        while page_indices_continues and i < log_units_len - 1:
            if len(tmp_unit) == 0:
                tmp_unit.extend([units[i], units[i + 1]])
                tmp_ids.extend([ids[i][1:].strip(), ids[i + 1][1:].strip()])
            else:
                tmp_unit.append(units[i + 1])
                tmp_ids.append(ids[i + 1][1:].strip())
            i += 1
            toks = re.findall(r"\w+|\W+", units[i].strip())
            page_indices = [i for i, t in enumerate(toks) if 'Page' in t]
            page_indices_continues = [i for i in page_indices if '#' not in toks[i - 1]]

        if len(tmp_unit) > 0:
            units_joined.append(" ".join(tmp_unit))
            unit_ids_joined.append(" ".join(tmp_ids))

        else:
            units_joined.append(units[i])
            unit_ids_joined.append(ids[i].strip())
        i += 1
    # add the latest logical unit (i == log_units_len - 1) to the list
    if i == log_units_len - 1:
        units_joined.append(units[i])
        unit_ids_joined.append(ids[i].strip())

    return units_joined, unit_ids_joined


def get_units_len(log_units_join_pages, max_len):
    ar_ra = re.compile("^[ذ١٢٣٤٥٦٧٨٩٠ّـضصثقفغعهخحجدًٌَُلإإشسيبلاتنمكطٍِلأأـئءؤرلاىةوزظْلآآ]+$")
    ar_toks = []
    max_tok_nrs = []
    for l in log_units_join_pages:
        # print(l, "\n")
        tok = re.findall(r"\w+|\W+", l)
        ar_toks.append(sum(ar_ra.search(t) is not None for t in tok))
    if len(ar_toks) > 0:
        max_tok_nrs.extend([n for n in ar_toks])# if n > max_len])
    # print(max_tok_nrs)
    return max_tok_nrs


def write_chunk(cex, counter, file_id, text, ids_in_chunk, rec, target_path, thresh):
# def write_chunk(cex, counter, file_id, text, rec, target_path, thresh):

    id = file_id + ".log%d" % counter
    chunk = rec % (id, file_id, text, ", ".join(ids_in_chunk))
    cex.append(chunk)
    if counter % thresh == 0:
        with open(target_path + "%05d" % counter, "w", encoding="utf8") as ft:
            ft.write("\n".join(cex))
        cex = []
    return cex


# process all texts in OpenITI
def process_all(input_folder, target_folder):

    print("\nGenerating logical passim corpus with logical ids included ...\n")

    count = 1
    max_units_len = {}
    thresh = 1000  # threshold for both number of json record in each file and length of tokens in the "text" of each json.
    min_len = 100  # Min threshold for number of tokens in the "text" item of each json
    max_len = 1000  # Max threshold for number of tokens in the "text" item of each json

    for root, dirs, files in os.walk(input_folder):
        dirs[:] = [d for d in dirs if d not in zfunc.exclude]

        for file in files:
            # print("file: %s" % file)
            if re.search("^\d{4}\w+\.\w+\.\w+-\w{4}_logical(\.(mARkdown|inProgress|completed))?$", file):
                path_full = os.path.join(root, file)
                f_name = path_full.split("/")[-1]
                print(f_name)

                if "" in path_full:
                    # logical_chunking(path_full, thresh, min_len, max_len, target_folder)
                    # return
                    tmp = logical_chunking(path_full, thresh, min_len, max_len, target_folder)
                    count += tmp[0]
                    if len(tmp[1]) > 0:
                        tmp[1].sort()
                        max_units_len[f_name] = tmp[1]
                        # print(max_units_len)
                #     if count % 100 == 0:
                #         print()
                #         print("=============" * 2)
                #         print("Processed: %d" % count)
                #         print("=============" * 2)
                #         print()
                # if count == 100:
                #     break
                # else:
                #     continue
                # return
    # print(max_units_len)
    with open(target_folder + "_tokens_len", "w", encoding="utf8") as f_len:
        # json.dump(max_units_len, f_len, indent=4, ensure_ascii=False)
        writer = csv.writer(f_len, delimiter='\t')
        for k in max_units_len:
            # print(k, " &&", max_units_len[k])
            writer.writerow([k, max_units_len[k]])


main = "/home/rostam/projs/KITAB/ara1/selected/"
target = "/home/rostam/projs/KITAB/ara1/selected/log_chunks/"

process_all(main, target)
#
# print("Done!")

# /home/rostam/projs/KITAB/Sira/Ibn Ishaq by Source/OpenITI_sources/
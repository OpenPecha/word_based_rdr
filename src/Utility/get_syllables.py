import re

from botok import TSEK


def split_by_TSEK(string_to_split):
    pattern = r"[་]+"  # Removing multiple TSEKs
    replacement = "་"
    string_to_split = re.sub(pattern, replacement, string_to_split)
    split_pattern = TSEK
    splited_list = re.split(split_pattern, string_to_split)
    if len(splited_list) == 1:
        return splited_list
    for index, element in enumerate(splited_list):
        if element == "":
            splited_list[index - 1] += TSEK
            break
        if index == len(splited_list) - 1:
            break
        if splited_list[index + 1] != "":
            splited_list[index] += TSEK

    splited_list = list(filter(None, splited_list))
    return splited_list


def split_by_TSEK_without_TsekConcat(word_string):
    pattern = r"[་]+"
    replacement = "་"
    # Removing multiple TSEKs to one just one TSEK
    word_string = re.sub(pattern, replacement, word_string)
    split_pattern = TSEK
    # Spliting the string with TSEK
    word_tsek_splited_list = re.split(split_pattern, word_string)
    word_tsek_splited_list = list(filter(None, word_tsek_splited_list))
    return word_tsek_splited_list


if __name__ == "__main__":
    print(split_by_TSEK("ལ-ས་པ་"))

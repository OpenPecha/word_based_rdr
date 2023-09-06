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


if __name__ == "__main__":
    print(split_by_TSEK("ལ-ས་པ་"))

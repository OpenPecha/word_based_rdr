import os
import re

from src.word_segmentation_rules_generator.preprocessing.preprocessor import (
    adjust_spaces,
)
from src.word_segmentation_rules_generator.tagger.tagger import split_by_TSEK


def split_into_word_tag_list(tagged_file="TIB_test_maxmatched.txt.TAGGED"):
    """
    Input: file that is tagged by rdr rules
    Output:List with word or syllables with their associated tag (P,A,B,N,C)
    """
    current_dir = os.path.dirname(__file__)
    relative_path = "../data/" + tagged_file
    file_path = os.path.join(current_dir, relative_path)

    file = open(file_path, encoding="utf-8")
    contents = file.read()
    words_list = contents.split()
    word_tag_list = []
    for word in words_list:
        word_tag_splited = word.split("/")
        if word_tag_splited[1] == "P":
            # If there is an affix involved,then there needs to be a space
            pattern = "-"
            replacement = " -"
            word_tag_splited[0] = re.sub(pattern, replacement, word_tag_splited[0])
            word_tag_list.append(word_tag_splited)
        else:
            syls_list = split_by_TSEK(word_tag_splited[0])
            # ['ལོག་པ-འོ', 'C'], in cases like here where there are two syllables in a word but only one tag
            if len(syls_list) != len(word_tag_splited[1]):
                anomaly_word_tag_list = adjust_anomaly_tagged(
                    syls_list, word_tag_splited
                )
                word_tag_list = word_tag_list + anomaly_word_tag_list
            else:
                for i in range(len(syls_list)):
                    word_tag_list.append([syls_list[i], word_tag_splited[1][i]])
    word_tag_list = adjust_affix_with_tag(word_tag_list)
    return word_tag_list


def adjust_anomaly_tagged(syls_list, word_tag_splited):
    """
    In some cases, for words that are not perfectly tagged, RDR is not tagging the same number
    as the syllables as its supposed to i.e, ['ལོག་པ-འོ', 'C'],
    Input: ['ལོག་པ-འོ', 'C']
    Output: ['ལོག་', 'C','པ-འོ','C']
    """
    anomaly_word_tag_list = []
    for i in range(len(syls_list)):
        if i < len(word_tag_splited[1]):
            anomaly_word_tag_list.append([syls_list[i], word_tag_splited[1][i]])
        else:
            anomaly_word_tag_list.append([syls_list[i], "C"])
    return anomaly_word_tag_list


def adjust_affix_with_tag(word_tag_list):
    for i in range(len(word_tag_list)):
        if word_tag_list[i][1] in ["P", "N", "C"]:
            # If there is an affix involved,then there needs to be a space
            pattern = "-"
            replacement = " -"
            word_tag_list[i][0] = re.sub(pattern, replacement, word_tag_list[i][0])
        else:  # So the tag is either A or B
            pattern = "-"
            replacement = " -"
            match = re.search(pattern, word_tag_list[i][0])
            if match:
                word_tag_list[i][0] = re.sub(pattern, replacement, word_tag_list[i][0])
            else:
                pattern = r"(ར|ས|འི|འམ|འང|འོ|འིའོ|འིའམ|འིའང|འོའམ|འོའང)"
                replacement = r" -\1"
                word_tag_list[i][0] = re.sub(pattern, replacement, word_tag_list[i][0])
    return word_tag_list


def split_merge_to_proper_string(tagged_file="TIB_test_maxmatched.txt.TAGGED"):
    """
    Input: tagged file, each word followed by \\ slash and tag predicted by rdr
    Output: string that is joined according to the tag
    """
    word_tag_list = split_into_word_tag_list(tagged_file)
    joined_string = ""
    for i in range(len(word_tag_list)):
        if word_tag_list[i][1] == "P":
            joined_string += word_tag_list[i][0] + " "
        else:
            if word_tag_list[i][1] in ["A", "N"]:
                joined_string += " "
            joined_string += word_tag_list[i][0]
            if word_tag_list[i + 1][1] in ["A", "N", "P"]:
                joined_string += " "
    joined_string = adjust_spaces(joined_string)
    return joined_string

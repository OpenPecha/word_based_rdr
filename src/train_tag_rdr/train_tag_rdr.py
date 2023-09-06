import os
import re
import sys
from pathlib import Path

# Add the root directory of your project to sys.path
root_path = (
    Path(__file__).resolve().parents[2]
)  # Adjust the number of parents as needed
sys.path.append(str(root_path))

from src.RDRPOSTagger.pSCRDRtagger.ExtRDRPOSTagger import ExtRDR_RUN  # noqa
from src.RDRPOSTagger.pSCRDRtagger.RDRPOSTagger import run  # noqa


def train_rdr(file_to_train_tagged="TIB_train_maxmatched_tagged.txt", THRESHOLD=(4, 4)):
    """
    Input: File already tagged, output from botok and then through tagger file
    Output: Two files i)RDR rules .RDR ii)RDR dictionary .DICT
    Important note: File should be in the folder 'data', and output in 'resources'
    """
    current_dir = os.path.dirname(__file__)
    relative_path = "../data/" + file_to_train_tagged
    file_path = os.path.join(current_dir, relative_path)
    function_arguments = ["RDRPOSTagger.py", "train", file_path, THRESHOLD]
    run(function_arguments)


def train_with_external_rdr(gold_corpus, external_tagged_corpus, THRESHOLD=(1, 1)):

    """
    Input: Gold standard corpus, tagged_string by external tagger(already rdr rules tagged on botok output), threshold
    return rdr rules in string
    """

    function_arguments = [
        "ExtRDRPOSTagger.py",
        "train",
        gold_corpus,
        external_tagged_corpus,
        THRESHOLD,
    ]
    return ExtRDR_RUN(function_arguments)


def train_file_with_external_rdr(
    gold_corpus_file="TIB_train_maxmatched_tagged.txt", THRESHOLD=(4, 4)
):
    """
    Input: File already tagged, output from botok and then through tagger file
    Output: Two files i)RDR rules .RDR ii)RDR dictionary .DICT
    Important note: File should be in the folder 'data', and output in 'resources'
    """
    current_dir = os.path.dirname(__file__)
    relative_path = "../data/" + gold_corpus_file
    file_path = os.path.join(current_dir, relative_path)
    gold_corpus = ""
    with open(file_path, encoding="utf-8") as file:
        gold_corpus = file.read()

    pattern = r"/[BIUXY]+"
    replacement = r"/U"
    external_tagged_corpus = re.sub(pattern, replacement, gold_corpus)
    result = train_with_external_rdr(gold_corpus, external_tagged_corpus, THRESHOLD)
    return result


def tag_with_ExtRDR(
    string_to_tag,
    RDR_rules="TIB_train_maxmatched_tagged.txt.RDR",
):
    """
    Input : String that is already went through botok max matched algorithm and word segmented,
    Output: file tagged acccording to the RDR model rules and dictionary.
    Important note: File should be in the folder 'data', and output in 'resources'
    """
    current_dir = os.path.dirname(__file__)
    # file_relative_path = "../data/" + file_to_tag
    rdr_rules_relative_path = "../data/" + RDR_rules

    # file_path = os.path.join(current_dir, file_relative_path)
    rdr_rules_path = os.path.join(current_dir, rdr_rules_relative_path)

    function_arguments = [
        "ExtRDRPOSTagger.py",
        "tag",
        rdr_rules_path,
        string_to_tag,
    ]
    return ExtRDR_RUN(function_arguments)


def tag_rdr(
    string_to_tag,
    RDR_rules="TIB_train_maxmatched_tagged.txt.RDR",
    RDR_dictionary="TIB_train_maxmatched_tagged.txt.DICT",
):
    """
    Input : String that is already went through botok max matched algorithm and word segmented,
    Output: file tagged acccording to the RDR model rules and dictionary.
    Important note: File should be in the folder 'data', and output in 'resources'
    """
    current_dir = os.path.dirname(__file__)
    # file_relative_path = "../data/" + file_to_tag
    rdr_rules_relative_path = "../data/" + RDR_rules
    RDR_dictionary_relative_path = "../data/" + RDR_dictionary

    # file_path = os.path.join(current_dir, file_relative_path)
    rdr_rules_path = os.path.join(current_dir, rdr_rules_relative_path)
    rdr_dict_path = os.path.join(current_dir, RDR_dictionary_relative_path)

    function_arguments = [
        "RDRPOSTagger.py",
        "tag",
        rdr_rules_path,
        rdr_dict_path,
        string_to_tag,
    ]
    return run(function_arguments)


def tag_file_rdr(
    file_to_tag="TIB_test_maxmatched.txt",
    file_format=True,
    RDR_rules="TIB_train_maxmatched_tagged.txt.RDR",
    RDR_dictionary="TIB_train_maxmatched_tagged.txt.DICT",
):

    current_dir = os.path.dirname(__file__)
    # file_relative_path = "../data/" + file_to_tag
    file_to_tag_relative_path = "../data/" + file_to_tag
    file_to_tag_path = os.path.join(current_dir, file_to_tag_relative_path)

    file = open(file_to_tag_path, encoding="utf-8")
    file_content = file.read()
    rdr_tagged_output = tag_rdr(file_content, RDR_rules, RDR_dictionary)
    if file_format:
        with open(file_to_tag_path + ".TAGGED", "w", encoding="utf-8") as file:
            # Write the content to the file
            file.write(rdr_tagged_output)
    else:
        return rdr_tagged_output


if __name__ == "__main__":

    result = train_file_with_external_rdr("TIB_train_maxmatched_tagged.txt", (3, 2))
    print(result)
    with open(
        "src/data/TIB_train_maxmatched_tagged.txt.RDR", "w", encoding="utf-8"
    ) as file:
        file.write(result)

    # tag_with_ExtRDR(
    #         r"src\data\TIB_short_test_maxmatched.txt", "TIB_train_maxmatched_tagged.txt.RDR"
    #     )

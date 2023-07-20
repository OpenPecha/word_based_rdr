import os

from ..RDRPOSTagger.pSCRDRtagger.ExtRDRPOSTagger import ExtRDR_RUN
from ..RDRPOSTagger.pSCRDRtagger.RDRPOSTagger import run


def train_rdr(file_to_train_tagged="TIB_train_maxmatched_tagged.txt", THRESHOLD=(3, 2)):
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


def train_with_external_rdr(gold_corpus_file, external_tagged_file, THRESHOLD=(1, 1)):

    """
    Input: Gold standard corpus, tagged file by external tagger, threshold
    Output: Two files i)RDR rules .RDR
    """
    current_dir = os.path.dirname(__file__)
    gold_corpus_relative_path = "../data/" + gold_corpus_file
    gold_corpus_file_path = os.path.join(current_dir, gold_corpus_relative_path)

    external_tagged_file_relative_path = "../data/" + external_tagged_file
    external_tagged_file_path = os.path.join(
        current_dir, external_tagged_file_relative_path
    )

    function_arguments = [
        "ExtRDRPOSTagger.py",
        "train",
        gold_corpus_file_path,
        external_tagged_file_path,
        THRESHOLD,
    ]
    ExtRDR_RUN(function_arguments)


def tag_rdr(
    string_to_tag,
    RDR_rules="TIB_train_maxmatched_tagged.txt.RDR",
    RDR_dictionary="TIB_train_maxmatched_tagged.txt.DICT",
):
    """
    Input : file that is already went through botok max matched algorithm and word segmented,
    Output: file tagged acccording to the RDR model rules and dictionary.
    Important note: File should be in the folder 'data', and output in 'resources'
    """
    current_dir = os.path.dirname(__file__)
    # file_relative_path = "../data/" + file_to_tag
    rdr_rules_relative_path = "../resources/" + RDR_rules
    RDR_dictionary_relative_path = "../resources/" + RDR_dictionary

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
    run(function_arguments)

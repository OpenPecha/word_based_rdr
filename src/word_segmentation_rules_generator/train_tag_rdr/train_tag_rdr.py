import os

from ..RDRPOSTagger.pSCRDRtagger.RDRPOSTagger import run


def train_rdr(file_to_train_tagged="TIB_tagged.txt"):
    current_dir = os.path.dirname(__file__)
    relative_path = "..\\data\\" + file_to_train_tagged
    file_path = os.path.join(current_dir, relative_path)
    function_arguments = ["RDRPOSTagger.py", "train", file_path]
    run(function_arguments)


def tag_rdr(
    file_to_tag="TIB_test_maxmatched.txt",
    RDR_rules="TIB_tagged.txt.RDR",
    RDR_dictionary="TIB_tagged.txt.DICT",
):
    current_dir = os.path.dirname(__file__)
    file_relative_path = "..\\data\\" + file_to_tag
    rdr_rules_relative_path = "..\\resources\\" + RDR_rules
    RDR_dictionary_relative_path = "..\\resources\\" + RDR_dictionary

    file_path = os.path.join(current_dir, file_relative_path)
    rdr_rules_path = os.path.join(current_dir, rdr_rules_relative_path)
    rdr_dict_path = os.path.join(current_dir, RDR_dictionary_relative_path)

    function_arguments = [
        "RDRPOSTagger.py",
        "tag",
        rdr_rules_path,
        rdr_dict_path,
        file_path,
    ]
    run(function_arguments)

import os

from ..RDRPOSTagger.pSCRDRtagger.RDRPOSTagger import run


def train_rdr(file_to_train_tagged="TIB_tagged.txt"):
    current_dir = os.path.dirname(__file__)
    relative_path = "..\\data\\" + file_to_train_tagged
    file_path = os.path.join(current_dir, relative_path)
    function_arguments = ["RDRPOSTagger.py", "train", file_path]
    run(function_arguments)

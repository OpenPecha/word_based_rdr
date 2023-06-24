from ..RDRPOSTagger.pSCRDRtagger.RDRPOSTagger import run


def train_rdr(file_to_train_tagged="TIB_tagged.txt"):
    file_path = r".\data" + file_to_train_tagged
    function_arguments = ["RDRPOSTagger.py", "train", file_path]
    run(function_arguments)

import re
from pathlib import Path

from .RDRPOSTagger.pSCRDRtagger.ExtRDRPOSTagger import ExtRDR_RUN
from .RDRPOSTagger.pSCRDRtagger.RDRPOSTagger import run


def train_rdr(file_path: Path, THRESHOLD=(4, 4)):
    """
    Input: File already tagged(already tokenized and tagged)
    Output: Two files i)RDR rules .RDR ii)RDR dictionary .DICT
    """
    function_arguments = ["RDRPOSTagger.py", "train", file_path, THRESHOLD]
    run(function_arguments)


def train_with_external_rdr(
    gold_corpus_tagged: str, external_tagged_corpus: str, THRESHOLD=(4, 4)
):

    """
    Input: Gold standard corpus, tagged_string by external tagger, threshold
    return rdr rules in string
    """

    function_arguments = [
        "ExtRDRPOSTagger.py",
        "train",
        gold_corpus_tagged,
        external_tagged_corpus,
        THRESHOLD,
    ]
    return ExtRDR_RUN(function_arguments)


def train_file_with_external_rdr(file_path: Path, THRESHOLD=(4, 4)):
    """
    Input: File already tagged(already tokenized and tagged)
    Output: Two files i)RDR rules .RDR
    """

    gold_corpus = file_path.read_text(encoding="utf-8")
    pattern = r"/[BIUXY]+"
    replacement = r"/U"
    external_tagged_corpus = re.sub(pattern, replacement, gold_corpus)
    result = train_with_external_rdr(gold_corpus, external_tagged_corpus, THRESHOLD)
    return result


def tag_with_external_rdr(file_path: Path, rdr_file_path: Path):
    """
    Input : String that is already tokenized and tagged
    Output: file tagged acccording to the RDR model rules and dictionary.
    """

    function_arguments = [
        "ExtRDRPOSTagger.py",
        "tag",
        rdr_file_path,
        file_path,
    ]
    return ExtRDR_RUN(function_arguments)


def tag_rdr(text: str, rdr_file_path: Path, dict_file_path: Path):

    function_arguments = [
        "RDRPOSTagger.py",
        "tag",
        rdr_file_path,
        rdr_file_path,
        text,
    ]
    return run(function_arguments)


def tag_file_rdr(file_path: Path, rdr_file_path: Path, dict_file_path: Path):
    file_content = file_path.read_text(encoding="utf-8")
    rdr_tagged_output = tag_rdr(file_content, rdr_file_path, dict_file_path)
    return rdr_tagged_output


if __name__ == "__main__":

    file_path = Path("src/data/TIB_train_maxmatched_tagged.txt")
    result = train_file_with_external_rdr(file_path, (3, 2))
    print(result)
    with open(
        "src/data/TIB_train_maxmatched_tagged.txt.RDR", "w", encoding="utf-8"
    ) as file:
        file.write(result)

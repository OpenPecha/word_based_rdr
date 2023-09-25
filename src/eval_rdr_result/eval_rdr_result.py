import os
import re
import sys
from pathlib import Path

# Add the root directory of your project to sys.path
root_path = (
    Path(__file__).resolve().parents[2]
)  # Adjust the number of parents as needed
sys.path.append(str(root_path))

from src.RDRPOSTagger.Utility.Eval import computeAccuracies, computeAccuracy  # noqa
from src.train_tag_rdr import tag_with_external_rdr  # noqa


def eval_rdr_result(
    goldStandardCorpus="TIB_train_maxmatched_tagged.txt",
    taggedCorpus="TIB_train_maxmatched.txt.TAGGED",
):
    """
    Input: Two files i)goldStandardCorpus: taggedfile from tagger.py based on botok maxmatch and gold corpus
                     ii)taggedCorpus: result from the rdr rules and dictionary
    Ouput: Accuracy of the tagged file
    """
    current_dir = os.path.dirname(__file__)
    goldCorpus_relative_path = "../data/" + goldStandardCorpus
    goldCorpus_file_path = os.path.join(current_dir, goldCorpus_relative_path)

    taggedCorpus_relative_path = "../data/" + taggedCorpus
    taggedCorpus_file_path = os.path.join(current_dir, taggedCorpus_relative_path)

    return computeAccuracy(goldCorpus_file_path, taggedCorpus_file_path)


def eval_rdr_known_unknown_result(
    goldStandardCorpus="TIB_train_maxmatched_tagged.txt",
    taggedCorpus="TIB_train_maxmatched.txt.TAGGED",
    fulldictionary="TIB_train_maxmatched_tagged.txt.DICT",
):
    """
    Input: Two files i)goldStandardCorpus: taggedfile from tagger.py based on botok maxmatch and gold corpus
                     ii)taggedCorpus: result from the rdr rules and dictionary
    Ouput: Accuracy of the tagged file
    """
    current_dir = os.path.dirname(__file__)
    goldCorpus_relative_path = "../data/" + goldStandardCorpus
    goldCorpus_file_path = os.path.join(current_dir, goldCorpus_relative_path)

    taggedCorpus_relative_path = "../data/" + taggedCorpus
    taggedCorpus_file_path = os.path.join(current_dir, taggedCorpus_relative_path)

    fulldict_relative_path = "../data/" + fulldictionary
    fulldict_file_path = os.path.join(current_dir, fulldict_relative_path)

    return computeAccuracies(
        fulldict_file_path, goldCorpus_file_path, taggedCorpus_file_path
    )


if __name__ == "__main__":
    # Gold corpus data tagged
    gold_corpus_data_tagged = Path(
        "src/data/TIB_train_maxmatched_tagged.txt"
    ).read_text(encoding="utf-8")
    pattern = r"/[BIUXY]+"
    replacement = r"/U"

    # Botok predicted data tagged
    botok_predicted_data = re.sub(pattern, replacement, gold_corpus_data_tagged)
    with open(
        "src/data/TIB_train_botok_tagged.txt.TAGGED", "w", encoding="utf-8"
    ) as tsvfile:
        tsvfile.write(botok_predicted_data)
    botok_acc = eval_rdr_result(
        "TIB_train_maxmatched_tagged.txt", "TIB_train_botok_tagged.txt.TAGGED"
    )
    print(f"botok accuracy: {botok_acc}")

    file_to_tag = Path("src/data/TIB_train_maxmatched.txt")
    rdr_file_path = Path("src/data/TIB_train_maxmatched_tagged.txt.RDR")
    tag_with_external_rdr(file_to_tag, rdr_file_path)
    # evaluating with result
    rdr_acc = eval_rdr_result(
        "TIB_train_maxmatched_tagged.txt", "TIB_train_maxmatched.txt.TAGGED"
    )
    print(f"botok + rdr accuracy: {rdr_acc}")

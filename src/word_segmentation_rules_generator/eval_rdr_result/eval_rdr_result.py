import os

from ..RDRPOSTagger.Utility.Eval import computeAccuracies, computeAccuracy


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

    fulldictionary = "TIB_train_maxmatched_tagged.txt.DICT"
    fulldict_relative_path = "../data/" + fulldictionary
    fulldict_file_path = os.path.join(current_dir, fulldict_relative_path)

    return computeAccuracies(
        fulldict_file_path, goldCorpus_file_path, taggedCorpus_file_path
    )

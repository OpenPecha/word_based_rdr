from pathlib import Path

from .config import PARENT_DIR
from .RDRPOSTagger.Utility.Eval import computeAccuracies, computeAccuracy


def eval_rdr_result(gold_corpus_file_path: Path, tagged_corpus_file_path: Path):
    gold_corpus_file_path = PARENT_DIR / gold_corpus_file_path
    tagged_corpus_file_path = PARENT_DIR / tagged_corpus_file_path
    return computeAccuracy(gold_corpus_file_path, tagged_corpus_file_path)


def eval_rdr_known_unknown_result(
    gold_corpus_file_path: Path, tagged_corpus_file_path: Path, dict_file_path: Path
):
    return computeAccuracies(
        dict_file_path, gold_corpus_file_path, tagged_corpus_file_path
    )

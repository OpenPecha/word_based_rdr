from pathlib import Path

from src.rdr_segmentation_accuracy import eval_rdr_result


def test_eval_rdr_result():
    gold_corpus_file_path = Path("tests/data/TIB_test_maxmatched_tagged.txt")
    tagged_corpus_file_path = Path("tests/data/TIB_test_maxmatched.txt.TAGGED")

    result_value = eval_rdr_result(gold_corpus_file_path, tagged_corpus_file_path)
    print(result_value)
    assert isinstance(result_value, float), "The value is not a float"

from src.word_segmentation_rules_generator.eval_rdr_result.eval_rdr_result import (
    eval_rdr_result,
)


def test_eval_rdr_result():
    result_value = eval_rdr_result(
        goldStandardCorpus="TIB_short_test_maxmatched_tagged.txt",
        taggedCorpus="TIB_short_test_maxmatched.txt.TAGGED",
    )
    print(result_value)
    assert isinstance(result_value, float), "The value is not a float"

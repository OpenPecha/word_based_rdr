from src.word_segmentation_rules_generator.eval_rdr_result.eval_rdr_result import (
    eval_rdr_result,
)


def test_eval_rdr_result():
    result_value = eval_rdr_result(
        goldStandardCorpus="TIB_train_maxmatched_tagged.txt",
        taggedCorpus="TIB_train_maxmatched.txt.TAGGED",
    )
    assert isinstance(result_value, float), "The value is not a float"

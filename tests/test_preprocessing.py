from src.project_name.preprocessing.preprocessor import (
    file_2_botok,
    gold_corpus_2_tagger,
)


def test_file_2_botok():
    assert (
        file_2_botok("༄༅། །རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེ-འི་ ཕྲེང་བ།")
        == "རྒྱལ་པོ་ལ་གཏམ་བྱ་བ་རིན་པོ་ཆེའི་ཕྲེང་བ་"
    )


def test_gold_corpus_2_tagger():
    assert (
        gold_corpus_2_tagger("༄༅། །རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེ-འི་ ཕྲེང་བ།")
        == "རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེའི་ ཕྲེང་བ་ "
    )

from src.word_segmentation_rules_generator.preprocessing.preprocessor import (
    file_2_botok,
    gold_corpus_2_tagger,
)


# Test function for file string to have no gap, so that there wont be bias before sending it to botok max match
def test_file_2_botok():
    assert (
        file_2_botok(
            "༄༅། །རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེ འི་ ཕྲེང་་་བ། ལ་ ལ་ལ་ ལ་ ལ་བ་ ཡོད། དཔལ། དགེའོ་ བཀྲ་ཤིས་ ཤོག།"
        )
        == "༄༅། །རྒྱལ་པོ་ལ་གཏམ་བྱ་བ་རིན་པོ་ཆེའི་ཕྲེང་་་བ། ལ་ལ་ལ་ལ་ལ་བ་ཡོད། དཔལ། དགེའོ་བཀྲ་ཤིས་ཤོག།"
    )


# Test function for gold corpus going into tagger
def test_gold_corpus_2_tagger():
    assert (
        gold_corpus_2_tagger(
            "༄༅། །རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེ འི་ ཕྲེང་་་བ། ལ་ ལ་ལ་ ལ་ ལ་བ་ ཡོད། དཔལ། དགེའོ་ བཀྲ་ཤིས་ ཤོག།"
        )
        == "༄༅།_། རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེ-འི་ ཕྲེང་་་བ །_ ལ་ ལ་ལ་ ལ་ ལ་བ་ ཡོད །_ དཔལ །_ དགེའོ་ བཀྲ་ཤིས་ ཤོག ། "
    )

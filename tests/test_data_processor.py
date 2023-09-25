from src.data_processor import (
    prepare_gold_corpus_for_tokenizer,
    transform_gold_corpus_for_tagging,
)


# Test function for file string to have no gap, so that there wont be bias before sending it to botok max match
def test_prepare_gold_corpus_for_tokenizer():
    assert (
        prepare_gold_corpus_for_tokenizer(
            "༄༅། །རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེ འི་ ཕྲེང་་་བ། ལ་ ལ་ལ་ ལ་ ལ་བ་ ཡོད། དཔལ། དགེའོ་ བཀྲ་ཤིས་ ཤོག།"
        )
        == "༄༅། །རྒྱལ་པོ་ལ་གཏམ་བྱ་བ་རིན་པོ་ཆེའི་ཕྲེང་་་བ། ལ་ལ་ལ་ལ་ལ་བ་ཡོད། དཔལ། དགེའོ་བཀྲ་ཤིས་ཤོག།"
    )


# Test function for gold corpus going into tagger
def test_transform_gold_corpus_for_tagging():
    assert (
        transform_gold_corpus_for_tagging(
            "༄༅། །རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེ འི་ ཕྲེང་་་བ། ལ་ ལ་ལ་ ལ་ ལ་བ་ ཡོད། དཔལ། དགེའོ་ བཀྲ་ཤིས་ ཤོག།"
        )
        == "༄༅།_། རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེ-འི་ ཕྲེང་་་བ །_ ལ་ ལ་ལ་ ལ་ ལ་བ་ ཡོད །_ དཔལ །_ དགེའོ་ བཀྲ་ཤིས་ ཤོག ། "
    )

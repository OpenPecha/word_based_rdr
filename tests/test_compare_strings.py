from rules_generator.compare_strings import compare_gold_corpus_and_tokenized_output


def test_compare_gold_corpus_and_tokenized_output():
    assert (
        compare_gold_corpus_and_tokenized_output(
            "༄༅། །རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེ འི་ ཕྲེང་་་བ། ལ་ ལ་ལ་ ལ་ ལ་བ་ ཡོད། དཔལ། དགེའོ་ བཀྲ་ཤིས་ ཤོག།"
        )[0]
        is True
    )

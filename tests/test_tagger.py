from botok import WordTokenizer

from rules_generator.data_processor import transform_gold_corpus_for_tagging
from rules_generator.tagger import tagger
from rules_generator.tokenizer_pipeline import botok_word_tokenizer_pipeline


def test_tagger():
    gold_corpus = "༄༅། །རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེ འི་ ཕྲེང་་་བ། ལ་ ལ་ལ་ ལ་ ལ་བ་ ཡོད། དཔལ། དགེའོ་ བཀྲ་ཤིས་ ཤོག།"
    gold_corpus_cleaned = transform_gold_corpus_for_tagging(gold_corpus)
    tokenized_output = botok_word_tokenizer_pipeline(WordTokenizer(), gold_corpus)
    tagger_output = tagger(gold_corpus_cleaned, tokenized_output)
    expected_output = "༄༅།_།_/U རྒྱལ་པོ་/U ལ་/U གཏམ་/U བྱ་བ་/U རིན་པོ་ཆེ-འི་/U ཕྲེང་་་བ/U _།_/U ལ་ལ་/BB ལ་ལ་/IB ལ་བ་/U ཡོད/U _།_/U དཔལ/U _།_/U དགེ-འོ་/B བཀྲ་ཤིས་ཤོག/BIB _།/U"  # noqa
    assert tagger_output == expected_output


if __name__ == "__main__":
    test_tagger()

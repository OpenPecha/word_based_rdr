from src.word_segmentation_rules_generator.max_matcher.max_matcher import (
    botok_max_matcher,
)


# The input is a gold corpus, but the string is preprocessed(no spaces) before botok does max match, so there
# be no bias
def test_botok_max_matcher():
    assert (
        botok_max_matcher(
            "༄༅། །རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེ འི་ ཕྲེང་་་བ། ལ་ ལ་ལ་ ལ་ ལ་བ་ ཡོད། དཔལ། དགེའོ་ བཀྲ་ཤིས་ ཤོག།"
        )
        == "༄༅།_། རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེ-འི་ ཕྲེང་་་བ །_ ལ་ལ་ ལ་ལ་ ལ་བ་ ཡོད །_ དཔལ །_ དགེ-འོ་ བཀྲ་ཤིས་ཤོག །"
    )

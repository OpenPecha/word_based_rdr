from src.project_name.max_matcher.max_matcher import botok_max_matcher


def test_botok_max_matcher():
    assert (
        botok_max_matcher("༄༅། །རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེའི་ ཕྲེང་བ།")
        == " རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེའི་ ཕྲེང་བ་  "
    )

from src.word_segmentation_rules_generator.comparator.comparator import comparator


def test_comparator():
    assert (
        comparator(
            "༄༅། །རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེ-འི་ hello ཕྲེང་བ། །ཡོན་ཏན་ ཀུན་ གྱིས་ བརྒྱན་པ་+པོ།"
        )[0]
        is True
    )
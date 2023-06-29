from src.word_segmentation_rules_generator.tagger.tagger import tagger


def test_tagger():
    assert (
        tagger(
            "༄༅། །རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེ འི་ ཕྲེང་་་བ། ལ་ ལ་ལ་ ལ་ ལ་བ་ ཡོད། དཔལ། དགེའོ་ བཀྲ་ཤིས་ ཤོག།"
        )
        == "༄༅།_།/P རྒྱལ་པོ་/P ལ་/P གཏམ་/P བྱ་བ་/P རིན་པོ་ཆེ-འི་/P ཕྲེང་་་བ/P །_/P ལ་ལ་/NN ལ་ལ་/CN ལ་བ་/P ཡོད/P །_/P དཔལ/P །_/P དགེ-འོ་/N བཀྲ་ཤིས་ཤོག/NCN །/P "  # noqa
    )

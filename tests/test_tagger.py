from src.project_name.tagger.tagger import tagger


def test_tagger():
    assert tagger("ལ་ ལ་ལ་ ལ་ ལ་བ་") == "ལ་ལ་/NN ལ་ལ་/CN ལ་བ་/P "

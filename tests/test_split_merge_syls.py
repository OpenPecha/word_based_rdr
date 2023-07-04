from src.word_segmentation_rules_generator.rdr_2_cql.split_merge_syls import (
    split_merge_to_proper_string,
)


def test_split_merge_syls():
    """
    Testing the function split_merge_to_proper_string
    the file is tagged with rdr
    and outputs the words in proper way
    """
    joined_string = split_merge_to_proper_string("TIB_short_test_maxmatched.txt.TAGGED")
    assert (
        joined_string
        == "༄༅།_། སྐྱེས་པ -འི་ རབས་ ཀྱི་ རྒྱ་ ཆེ -ར་ བཤད་པ །_༄༅༅།_། རྒྱ་གར་ སྐད་ དུ །_ ཛཱ་ ཏ་ ཀ་ མཱ་ ལཱ་ ཊཱི་ ཀཱ །_ བོད་སྐད་དུ །_ སྐྱེས་པ -འི་ རབས་ ཀྱི་ རྒྱ་ ཆེ -ར་ བཤད་པ །_ བཅོམ་ལྡན་འདས་ ངག་ གི་ དབང་པོ་ ལ་ ཕྱག་འཚལ་ ལོ །_། ཐུབ་པ -འི་ ལེགས་ སྤྱོད་ རྨད་བྱུང་ དཔག་མེད་པ །_། སྙན་ངག་ མཁན་པོ་ འཕགས་པ་ དཔའ་བོ -ས་ བཀོད །_། བདག་ བློ་ ཞན་ ཀྱང་ གུས་པ -ས་ བཤད་པ་ ནི །_། བློ་ ཆུང་ དག་ ལ་ པན་ ཕྱིར་ རབ་ཏུ་ བརྩམས །_།"  # noqa
    )

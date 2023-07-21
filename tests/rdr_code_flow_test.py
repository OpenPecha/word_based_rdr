from src.word_segmentation_rules_generator.max_matcher.max_matcher import (
    botok_max_matcher,
)
from src.word_segmentation_rules_generator.tagger.tagger import tagger
from src.word_segmentation_rules_generator.train_tag_rdr.train_tag_rdr import tag_rdr


def print_code_flow():
    gold_standard_string = "༄༅། །རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེ འི་ ཕྲེང་་་བ། ལ་ ལ་ལ་ ལ་ ལ་བ་ ཡོད། དཔལ། དགེའོ་ བཀྲ་ཤིས་ ཤོག།"  # noqa
    input_string = "༄༅། །རྒྱལ་པོ་ལ་གཏམ་བྱ་བ་རིན་པོ་ཆེའི་ཕྲེང་་་བ། ལ་ལ་ལ་ལ་ལ་བ་ཡོད། དཔལ། དགེའོ་བཀྲ་ཤིས་ཤོག།"

    botok_output = botok_max_matcher(input_string)
    print("Botok output:> ", botok_output)

    tagger_output = tagger(gold_standard_string)
    print("Tagger output:> ", tagger_output)

    rdr_tag_output = tag_rdr(botok_output)
    print("RDR output:> ", rdr_tag_output)

import os
import sys

from src.max_matcher.max_matcher import botok_max_matcher
from src.rdr_2_cql.rdr_2_cql import rdr_2_cql_string
from src.tagger.tagger import tagger
from src.train_tag_rdr.train_tag_rdr import tag_rdr, train_with_external_rdr


def print_code_flow():
    gold_standard_string = (
        "ལ་ ལ་ལ་ ལ་ ལ་བ་ ཡོད། ལ་ ལ་ ལ་བ་ ཡོད། མི་ ལ་ལ་ ལ་ ལ་བ་ ཡོད།"  # noqa
    )
    input_string = "ལ་ལ་ལ་ལ་ལ་བ་ཡོད། ལ་ལ་ལ་བ་ཡོད། མི་ལ་ལ་ལ་ལ་བ་ཡོད།"

    print("Gold output:> ", gold_standard_string)

    botok_output = botok_max_matcher(input_string)
    print("Botok output:> ", botok_output)

    tagger_output = tagger(gold_standard_string)
    print("Tagger output:> ", tagger_output)

    # Redirect the standard output to the null device
    sys.stdout = open(os.devnull, "w")
    rdr_tag_output = tag_rdr(botok_output)
    # After your code is executed, restore the standard output
    sys.stdout = sys.__stdout__
    print("RDR output:> ", rdr_tag_output)

    rdr_rules = train_with_external_rdr(tagger_output, rdr_tag_output)
    print("RDR Rules generated:---------------------------> ")
    print(rdr_rules)

    cql_rules = rdr_2_cql_string(rdr_rules)
    print("CQL Rules generated:---------------------------> ")
    print(cql_rules)

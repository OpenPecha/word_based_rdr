import re
from pathlib import Path

from .rdr_to_cql import convert_rdr_to_cql
from .tagger import tagger
from .train_tag_rdr import train_with_external_rdr


def convert_tags_to_perfect_tag(text: str) -> str:
    """
    Input: Text with tags
    Output: Text with perfect tags
    Eg: 'ལ་ལ་/BB ལ་ལ་/BB ལ་བ་/U ཡོད་/U' -> 'ལ་ལ་/U ལ་ལ་/U ལ་བ་/U ཡོད་/U'
    """

    pattern = r"/[BIUXY]+"
    replacement = r"/U"
    return re.sub(pattern, replacement, text)


def pipeline(gold_corpus):
    tagger_output = tagger(gold_corpus)

    external_tagger_output = convert_tags_to_perfect_tag(tagger_output)
    rdr_rules = train_with_external_rdr(tagger_output, external_tagger_output, (3, 2))
    cql_rules = convert_rdr_to_cql(rdr_rules)
    return cql_rules


if __name__ == "__main__":
    gold_corpus = Path("src/data/TIB_train.txt").read_text(encoding="utf-8")
    cql_rules = pipeline(gold_corpus)
    print(cql_rules)
    # with open("src/data/TIB_demo.tsv", "w", encoding="utf-8") as tsvfile:
    #     tsvfile.write(cql_rules)

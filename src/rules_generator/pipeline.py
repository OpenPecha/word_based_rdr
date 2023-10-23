import re
from pathlib import Path

from rules_generator.rdr_to_cql import convert_rdr_to_cql
from rules_generator.tagger import tagger
from rules_generator.train_tag_rdr import train_with_external_rdr


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
    DATA_DIR = Path(__file__).resolve().parent / "data"

    with open(DATA_DIR / "gold_corpus.TAGGED", "w", encoding="utf-8") as fileout:
        fileout.write(tagger_output)

    print("Tagging done....")
    external_tagger_output = convert_tags_to_perfect_tag(tagger_output)
    rdr_rules = train_with_external_rdr(tagger_output, external_tagger_output, (3, 2))
    with open(DATA_DIR / "gold_corpus.RDR", "w", encoding="utf-8") as fileout:
        fileout.write(rdr_rules)
    print("RDR rules done....")
    cql_rules = convert_rdr_to_cql(rdr_rules)
    with open(DATA_DIR / "gold_corpus.tsv", "w", encoding="utf-8") as fileout:
        fileout.write(cql_rules)
    print("CQL rules done....")
    return cql_rules


if __name__ == "__main__":
    DATA_DIR = Path(__file__).resolve().parent / "data"
    gold_corpus = Path(DATA_DIR / "gold_corpus.txt").read_text(encoding="utf-8")
    cql_rules = pipeline(gold_corpus)
    print(cql_rules)

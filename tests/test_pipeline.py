from pathlib import Path

from botok import WordTokenizer
from botok.config import Config
from botok.modifytokens.adjusttokens import AdjustTokens

from rules_generator.pipeline import pipeline


def test_cql_rules():
    config = Config(dialect_name="general", base_path=Path.home())
    wt = WordTokenizer(config=config)
    string = "ལ་ལ་ལ་ལ་ལ་བ་ཡོད་"

    token_list = wt.tokenize(string, split_affixes=False)
    token_text_list = [token.text for token in token_list]
    assert token_text_list == ["ལ་ལ་", "ལ་ལ་", "ལ་བ་", "ཡོད་"]

    gold_corpus = Path("tests/data/TIB_gold_corpus.txt").read_text(encoding="utf-8")
    # get cql rules from gold corpus
    cql_rules = pipeline(gold_corpus, num_parts=1)

    # write test adjust rule to file
    Path("tests/data/TIB_lala_test.tsv").write_text(cql_rules, encoding="utf-8")
    # add test adjust rule to adjustments rules
    wt.config.adjustments["rules"].append(Path("tests/data/TIB_lala_test.tsv"))
    at = AdjustTokens(
        main=wt.config.dictionary["rules"], custom=wt.config.adjustments["rules"]
    )
    adjusted = at.adjust(token_list)
    adjusted_token_text_list = [token.text for token in adjusted]
    assert adjusted_token_text_list == ["ལ་", "ལ་ལ་", "ལ་", "ལ་བ་", "ཡོད་"]


if __name__ == "__main__":
    test_cql_rules()

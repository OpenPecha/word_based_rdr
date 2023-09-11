from pathlib import Path

from botok import WordTokenizer
from botok.config import Config
from botok.modifytokens.adjusttokens import AdjustTokens


def test_cql_rules():
    config = Config(dialect_name="general", base_path=Path.home())
    wt = WordTokenizer(config=config)
    string = "མངོན་པར་"

    string = "ལ་ལ་ལ་ལ་ལ་བ་ཡོད་"

    token_list = wt.tokenize(string, split_affixes=False)
    token_text_list = [token.text for token in token_list]
    print(token_text_list)
    # add test adjust rule to adjustments rules
    wt.config.adjustments["rules"].append(Path("src/data/TIB_demo.tsv"))
    at = AdjustTokens(
        main=wt.config.dictionary["rules"], custom=wt.config.adjustments["rules"]
    )
    adjusted = at.adjust(token_list)
    adjusted_token_text_list = [token.text for token in adjusted]
    print(adjusted_token_text_list)


if __name__ == "__main__":
    test_cql_rules()

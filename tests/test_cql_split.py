from pathlib import Path

from botok import WordTokenizer
from botok.config import Config

# from botok.modifytokens.adjusttokens import AdjustTokens


def test_adjust_tokens():
    config = Config(dialect_name="general", base_path=Path.home())
    wt = WordTokenizer(config=config)

    string = "དེ་ནི་དད་པ་ཅན་ཞེས་བྱ།"

    token_list = wt.tokenize(string, split_affixes=False)
    print(token_list)

    # add test adjust rule to adjustments rules
    wt.config.adjustments["rules"].append(Path("tests/data/split_merge_test.tsv"))
    print("---------------------------------")

    token_list = wt.tokenize(string, split_affixes=False)
    print(token_list)
    # at = AdjustTokens(
    #     main = wt.config.dictionary["rules"], custom = wt.config.adjustments["rules"]
    # )
    # adjusted = at.adjust(token_list)
    # print(adjusted)


if __name__ == "__main__":
    test_adjust_tokens()

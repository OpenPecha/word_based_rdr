import sys
from pathlib import Path

from botok import Config
from botok.textunits.bosyl import BoSyl
from botok.tries.trie import Trie

# Add the root directory of your project to sys.path
root_path = (
    Path(__file__).resolve().parents[2]
)  # Adjust the number of parents as needed
sys.path.append(str(root_path))

from src.tagger.tagger import split_by_TSEK  # noqa


def get_POS(word_string):
    config = Config()
    trie = Trie(
        BoSyl,
        profile=config.profile,
        main_data=config.dictionary,
        custom_data=config.adjustments,
    )
    syls = split_by_TSEK(word_string)
    syls = ["ལ", "ལ"]
    current_node = None
    for i in range(len(syls)):
        syl = syls[i]
        current_node = trie.walk(syl, current_node)
    return current_node


if __name__ == "__main__":
    word_pos = get_POS("ལ་ལ་")
    print(word_pos)

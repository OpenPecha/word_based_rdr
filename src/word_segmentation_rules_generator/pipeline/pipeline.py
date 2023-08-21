import sys
from pathlib import Path

# Add the root directory of your project to sys.path
root_path = (
    Path(__file__).resolve().parents[3]
)  # Adjust the number of parents as needed
sys.path.append(str(root_path))

# Now import the modules from your project
from src.word_segmentation_rules_generator.comparator.comparator import (  # noqa
    is_equal_string_length,
)
from src.word_segmentation_rules_generator.eval_rdr_result.eval_rdr_result import (  # noqa
    eval_rdr_result,
)
from src.word_segmentation_rules_generator.max_matcher.max_matcher import (  # noqa
    botok_max_matcher,
)
from src.word_segmentation_rules_generator.preprocessing.preprocessor import (  # noqa
    file_2_botok,
    gold_corpus_2_tagger,
)
from src.word_segmentation_rules_generator.tagger.tagger import tagger  # noqa
from src.word_segmentation_rules_generator.train_tag_rdr.train_tag_rdr import (  # noqa
    tag_rdr,
    train_rdr,
)


def pipeline(data):
    gold_corpus = data
    gold_corpus_2_tagger_input = gold_corpus_2_tagger(data)  # noqa

    botok_input = file_2_botok(data)
    botok_output = botok_max_matcher(botok_input)

    is_equal_string_length_result = is_equal_string_length(  # noqa
        gold_corpus, botok_output
    )

    tagger_output = tagger(data)
    # print(tagger_output)

    trained_file = "TIB_train_temp.txt"
    trained_file_path = "../data/" + trained_file
    with open(trained_file_path, "w", encoding="utf-8") as file:
        file.write(tagger_output)

    train_rdr(trained_file_path)

    tagged_content = tag_rdr(
        botok_output, trained_file + ".RDR", trained_file + ".DICT"
    )
    tagged_file_path = "../data/TIB_train_maxmatched_temp.txt"
    with open(tagged_file_path, "w", encoding="utf-8") as file:
        file.write(tagged_content)

    accuracy_result = eval_rdr_result(
        "TIB_train_temp.txt", "TIB_train_maxmatched_temp.txt"
    )
    print(accuracy_result)


if __name__ == "__main__":
    file_string = Path("../data/TIB_gold.txt").read_text(encoding="utf-8")
    pipeline(file_string)

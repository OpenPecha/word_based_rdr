import sys
from pathlib import Path

# Add the root directory of your project to sys.path
root_path = (
    Path(__file__).resolve().parents[2]
)  # Adjust the number of parents as needed
sys.path.append(str(root_path))

# Now import the modules from your project
from src.comparator.comparator import is_equal_string_length  # noqa
from src.eval_rdr_result.eval_rdr_result import (  # noqa
    eval_rdr_known_unknown_result,
    eval_rdr_result,
)
from src.max_matcher.max_matcher import botok_max_matcher  # noqa
from src.preprocessing.preprocessor import file_2_botok, gold_corpus_2_tagger  # noqa
from src.tagger.tagger import tagger  # noqa
from src.train_tag_rdr.train_tag_rdr import tag_rdr, train_rdr  # noqa


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
    trained_file_path = "src/data/" + trained_file
    with open(trained_file_path, "w", encoding="utf-8") as file:
        file.write(tagger_output)

    train_rdr(trained_file)

    tagged_content = tag_rdr(
        botok_output, trained_file + ".RDR", trained_file + ".DICT"
    )
    tagged_file_path = "src/data/TIB_train_maxmatched_tagged_temp.txt"
    with open(tagged_file_path, "w", encoding="utf-8") as file:
        file.write(tagged_content)

    accuracy_result = eval_rdr_result(
        "TIB_train_temp.txt", "TIB_train_maxmatched_tagged_temp.txt"
    )
    print(accuracy_result)
    (
        training_countKN,
        training_countUNKN,
        training_numwords,
        known_training_acc,
        unknown_training_acc,
        overall_training_acc,
    ) = eval_rdr_known_unknown_result(
        "TIB_train_temp.txt",
        "TIB_train_maxmatched_tagged_temp.txt",
        "TIB_train_temp.txt.DICT",
    )
    print(
        "Training data values:> ",
        training_countKN,
        training_countUNKN,
        training_numwords,
    )
    print(
        "Training accuracy Value:> ",
        known_training_acc,
        unknown_training_acc,
        overall_training_acc,
    )


if __name__ == "__main__":
    file_string = Path("src/data/TIB_gold.txt").read_text(encoding="utf-8")
    pipeline(file_string)

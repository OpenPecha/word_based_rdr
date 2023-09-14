import re
import sys
from pathlib import Path

# Add the root directory of your project to sys.path
root_path = (
    Path(__file__).resolve().parents[2]
)  # Adjust the number of parents as needed
sys.path.append(str(root_path))

# Now import the modules from your project
from src.comparator.comparator import is_equal_string_length  # noqa
from src.data_processor import file_2_botok, gold_corpus_2_tagger  # noqa
from src.eval_rdr_result.eval_rdr_result import (  # noqa
    eval_rdr_known_unknown_result,
    eval_rdr_result,
)
from src.max_matcher.max_matcher import botok_max_matcher  # noqa
from src.rdr_2_cql.split_merge_cql import split_merge_cql  # noqa
from src.tagger.tagger import tagger  # noqa
from src.train_tag_rdr.train_tag_rdr import train_with_external_rdr  # noqa


def pipeline(data):
    # Pipeline description:>
    # The input data should be the gold corpus such that word segmented with spaces
    # gold_corpus = data
    # # Some data processing on gold corpus to have similar compare with botok output
    # gold_corpus_2_tagger_input = gold_corpus_2_tagger(data)  # noqa

    # # The gold corpus data is put together with no space allowed before sending to botok
    # botok_input = file_2_botok(data)
    # # Sending to botok and getting the maxmatched output
    # botok_output = botok_max_matcher(botok_input)

    # # This checks if the processing steps has done correctly and has equal string before sending to the tagger
    # is_equal_string_length_result = is_equal_string_length(  # noqa
    #     gold_corpus, botok_output
    # )

    # Sending the data to tagger,
    # In this step, all the above steps is done in tagger function, thats why previous variables has not been
    # passed as an argument
    tagger_output = tagger(data)

    # For External RDR, three arguments are needed
    # i) Tagged gold corpus: output from the tagger is given
    # ii) Tagged corpus by external tagger: output from botok
    # iii)Threshold value

    # Eg with a simple sentence:
    # data = 'ལ་ ལ་ལ་ ལ་ ལ་བ་ ཡོད་'
    # botok_output = 'ལ་ལ་ ལ་ལ་ ལ་བ་ ཡོད་'
    # tagger_output = 'ལ་ལ་\BB ལ་ལ་\BB ལ་བ་\U ཡོད་\U'
    # exteral_tagger_output = 'ལ་ལ་\U ལ་ལ་\U ལ་བ་\U ཡོད་\U'

    # Here all the tags are bieng replaced by 'U' because the word splited in tagger_output is from botok and
    # according to them, all the words are segmented perfectly
    pattern = r"/[BIUXY]+"
    replacement = r"/U"
    external_tagger_output = re.sub(pattern, replacement, tagger_output)
    rdr_rules = train_with_external_rdr(tagger_output, external_tagger_output, (3, 2))

    cql_rules = split_merge_cql(rdr_rules)
    return cql_rules


if __name__ == "__main__":
    file_string = Path("src/data/TIB_demo.txt").read_text(encoding="utf-8")
    cql_rules = pipeline(file_string)
    print(cql_rules)
    with open("src/data/TIB_demo.tsv", "w", encoding="utf-8") as tsvfile:
        tsvfile.write(cql_rules)

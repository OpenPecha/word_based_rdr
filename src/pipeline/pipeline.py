import re
from pathlib import Path

from ..compare_strings import compare_gold_corpus_and_tokenized_output  # noqa
from ..data_processor import (  # noqa
    prepare_gold_corpus_for_tokenizer,
    transform_gold_corpus_for_tagging,
)
from ..eval_rdr_result.eval_rdr_result import (  # noqa
    eval_rdr_known_unknown_result,
    eval_rdr_result,
)
from ..rdr_2_cql.split_merge_cql import split_merge_cql  # noqa
from ..tagger.tagger import tagger  # noqa
from ..tokenizer_pipeline import botok_word_tokenizer_pipeline  # noqa
from ..train_tag_rdr.train_tag_rdr import train_with_external_rdr  # noqa


def pipeline(data):
    # Pipeline description:>
    # The input data should be the gold corpus such that word segmented with spaces
    # gold_corpus = data
    # # Some data processing on gold corpus to have similar compare with botok output
    # transform_gold_corpus_for_tagging_input = transform_gold_corpus_for_tagging(data)  # noqa

    # # The gold corpus data is put together with no space allowed before sending to botok
    # botok_input = prepare_gold_corpus_for_tokenizer(data)
    # # Sending to botok and getting the maxmatched output
    # botok_output = botok_word_tokenizer_pipeline(botok_input)

    # # This checks if the processing steps has done correctly and has equal string before sending to the tagger
    # is_corpus_tokenization_identical_result = is_corpus_tokenization_identical(  # noqa
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

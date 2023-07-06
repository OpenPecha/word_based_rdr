import warnings

from botok import BoSyl, Config, TokChunks, Tokenize, Trie

from ..tagger.tagger import split_by_TSEK


def create_tokens(
    document_string="༄༅། ། རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ hello རིན་པོ་ཆེ འི་ ཕྲེང་བ ། ༄༅༅། ། རྒྱ་གར་ སྐད་ དུ །",
):
    # Ignore all warnings
    warnings.filterwarnings("ignore")

    config = Config()
    trie = Trie(
        BoSyl,
        profile=config.profile,
        main_data=config.dictionary,
        custom_data=config.adjustments,
    )
    word_list = document_string.strip().split()
    tokens = []
    for word in word_list:
        preprocessed = TokChunks(word, ignore_chars=None, space_as_punct=False)
        preprocessed.serve_syls_to_trie()
        tok = Tokenize(trie)
        tok.pre_processed = preprocessed
        syls = split_by_TSEK(word)
        syls_length = len(syls)
        syls_arg = [i for i in range(syls_length)]
        token = tok.chunks_to_token(syls_arg, {}, None)
        tokens.append(token)
    return tokens

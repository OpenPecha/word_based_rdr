import warnings

from botok import BoSyl, Config, TokChunks, Tokenize, Trie

# from botok.tokenizers.tokenize import Tokenize

# Ignore all warnings
warnings.filterwarnings("ignore")

# input_string = "ཀུན་་་དགའི་དོན་གྲུབ།"
# input_string = "༄༅།_། རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེ -འི་ ཕྲེང་བ །_༄༅༅།_། རྒྱ་གར་ སྐད་ དུ །_"
input_string = "རྒྱ་གར་ སྐད་ དུ། རཱ་ ཛ་པ་ རི་ ཀ་ ཐཱ་ རཏྣ་ མཱ་ ལཱི། བོད་སྐད་ དུ། རྒྱལ་པོ་ ལ་ གཏམ་ བྱ་བ་ རིན་པོ་ཆེ -འི་ ཕྲེང་བ། "  # noqa

config = Config()
trie = Trie(
    BoSyl,
    profile=config.profile,
    main_data=config.dictionary,
    custom_data=config.adjustments,
)
input_string_word_list = input_string.split()
for word in input_string_word_list:

    preproc = TokChunks(word)
    preproc.serve_syls_to_trie()
    syls = preproc.get_syls()
    tok = Tokenize(trie)
    tok.pre_processed = preproc
    syls = preproc.get_syls()
    print(tok.pre_processed.chunks, end=" ")
    print(syls)

# tokens = tok.chunks_to_token(syls, )

# print(preproc)

# print(syls)
#
# print(syls)
# tokens = tok.tokenize(preproc)
# print(*tokens, sep=f"{'='*65}\n\n")

# Reset the warning filter to its default behavior (optional)
warnings.filterwarnings("default")

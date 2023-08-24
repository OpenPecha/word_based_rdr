import re
from typing import Dict, List, Optional

from ..Utility.Get_token_attributes import Get_CONTENT_POS_attributes
from ..Utility.String_Manipulation import Remove_tag_in_String


class Object:
    attributes = [
        "word",
        "tag",
        "pos",
        "prevWord2",
        "prevWord1",
        "nextWord1",
        "nextWord2",
        "prevTag2",
        "prevTag1",
        "nextTag1",
        "nextTag2",
        "prevPos2",
        "prevPos1",
        "nextPos1",
        "nextPos2"
        # "suffixL2",
        # "suffixL3",
        # "suffixL4",
    ]
    # code = "def __init__(self"
    # for att in attributes:
    #     code = code + ", " + att + " = None"
    # code = code + "):\n"
    # for att in attributes:
    #     code = code + "    self." + att + "=" + att + "\n"

    # exec(code)

    # def toStr(self):
    #     res = "("
    #     for att in Object.attributes:
    #         boo = eval("isinstance(self. " + att + ", str)")
    #         if not boo:
    #             res = res + str(eval("self." + att))
    #         else:
    #             res = res + '"' + str(eval("self." + att)) + '"'

    #         if att != Object.attributes[len(Object.attributes) - 1]:
    #             res = res + ","
    #     res += ")"
    #     return res

    def __init__(self, *args):
        for attr, value in zip(self.attributes, args):
            setattr(self, attr, value)

    def toStr(self):
        res = "("
        for att in self.attributes:
            boo = isinstance(getattr(self, att), str)
            if not boo:
                res = res + str(getattr(self, att))
            else:
                res = res + '"' + str(getattr(self, att)) + '"'

            if att != self.attributes[-1]:
                res = res + ","
        res += ")"
        return res


def getWordTag(wordTag):
    if wordTag == "///":
        return "/", "/"
    index = wordTag.rfind("/")
    if index == -1:
        return None, None
    word = wordTag[:index].strip()
    tag = wordTag[index + 1 :].strip()  # noqa
    return word, tag


def getObject(wordTags, wordPOS, index):  # Sequence of "Word/Tag"
    word, tag = getWordTag(wordTags[index])
    pos = wordPOS[index]
    preWord1 = preTag1 = prePos1 = preWord2 = preTag2 = prePos2 = ""
    nextWord1 = nextTag1 = nextPos1 = nextWord2 = nextTag2 = nextPos2 = ""

    # suffixL2 = suffixL3 = suffixL4 = ""

    # decodedW = word
    # if len(decodedW) >= 4:
    #     suffixL3 = decodedW[-3:]
    #     suffixL2 = decodedW[-2:]
    # if len(decodedW) >= 5:
    #     suffixL4 = decodedW[-4:]

    if index > 0:
        preWord1, preTag1 = getWordTag(wordTags[index - 1])
        prePos1 = wordPOS[index - 1]
    if index > 1:
        preWord2, preTag2 = getWordTag(wordTags[index - 2])
        prePos2 = wordPOS[index - 2]
    if index < len(wordTags) - 1:
        nextWord1, nextTag1 = getWordTag(wordTags[index + 1])
        nextPos1 = wordPOS[index + 1]
    if index < len(wordTags) - 2:
        nextWord2, nextTag2 = getWordTag(wordTags[index + 2])
        nextPos2 = wordPOS[index + 2]

    return Object(
        word,
        tag,
        pos,
        preWord2,
        preWord1,
        nextWord1,
        nextWord2,
        preTag2,
        preTag1,
        nextTag1,
        nextTag2,
        prePos2,
        prePos1,
        nextPos1,
        nextPos2
        # suffixL2,
        # suffixL3,
        # suffixL4,
    )


def add_newline_to_shad(Corpus_string):
    pattern = r"([^ ]*།[^ ]*)"
    replacement = r"\1\n"
    new_Corpus = re.sub(pattern, replacement, Corpus_string)
    return new_Corpus


def getObjectDictionary(initializedCorpus, goldStandardCorpus, string_argument):

    if not string_argument:
        goldStandardCorpus = open(goldStandardCorpus, encoding="utf-8").read()
        initializedCorpus = open(initializedCorpus, encoding="utf-8").read()

    # Getting values for POS values
    init_without_tags = Remove_tag_in_String(initializedCorpus)
    POS_list = Get_CONTENT_POS_attributes(init_without_tags)

    goldStandardCorpus = add_newline_to_shad(goldStandardCorpus)
    initializedCorpus = add_newline_to_shad(initializedCorpus)

    goldStandardSens = goldStandardCorpus.splitlines()
    initializedSens = initializedCorpus.splitlines()

    objects: Dict[str, Dict[str, list]] = {}  # objects = {}

    j = 0
    counter = 0
    for i in range(len(initializedSens)):
        init = initializedSens[i].strip()

        if len(init) == 0:
            continue

        while j < len(goldStandardSens) and goldStandardSens[j].strip() == "":
            j += 1

        if j >= len(goldStandardSens):
            continue

        gold = goldStandardSens[j].strip()
        j += 1

        initWordTags = (
            init.replace("“", "''").replace("”", "''").replace('"', "''").split()
        )
        goldWordTags = (
            gold.replace("“", "''").replace("”", "''").replace('"', "''").split()
        )

        pos_list = POS_list[counter : counter + len(initWordTags)]  # noqa
        counter += len(initWordTags)

        for k in range(len(initWordTags)):
            initWordTags[k] = initWordTags[k].replace("_", " ")
            goldWordTags[k] = goldWordTags[k].replace("_", " ")

            initWord, initTag = getWordTag(initWordTags[k])
            goldWord, correctTag = getWordTag(goldWordTags[k])

            if initWord != goldWord:
                print(
                    "\nERROR (Raw texts are mismatched || Some sentence is incorrectly formatted):"
                )
                print(
                    str(i + 1) + "th initialized sentence:   " + " ".join(initWordTags)
                )
                print(
                    str(i + 1) + "th gold standard sentence: " + " ".join(goldWordTags)
                )
                return None

            if initTag not in objects.keys():
                objects[initTag] = {}
                objects[initTag][initTag] = []

            if correctTag not in objects[initTag].keys():
                objects[initTag][correctTag] = []

            objects[initTag][correctTag].append(getObject(initWordTags, pos_list, k))

    return objects


class FWObject:
    """
    RDRPOSTaggerV1.1: new implementation scheme
    RDRPOSTaggerV1.2: add suffixes
    """

    def __init__(self, check: bool = False):
        self.context: List[Optional[str]] = []
        if check is False:
            # self.context = [None] * 13
            self.context = [None] * 10
        else:
            # self.context = ["<W>", "<T>"] * 5 + ["<SFX>"] * 3  # type: ignore
            self.context = ["<W>", "<T>"] * 5
        self.notNoneIds: List[int] = []

    @staticmethod
    def getFWObject(startWordTags, index):
        object = FWObject(True)
        word, tag = getWordTag(startWordTags[index])
        object.context[4] = word
        object.context[5] = tag

        # decodedW = word
        # if len(decodedW) >= 4:
        #     object.context[10] = decodedW[-2:]
        #     object.context[11] = decodedW[-3:]
        # if len(decodedW) >= 5:
        #     object.context[12] = decodedW[-4:]

        if index > 0:
            preWord1, preTag1 = getWordTag(startWordTags[index - 1])
            object.context[2] = preWord1
            object.context[3] = preTag1

        if index > 1:
            preWord2, preTag2 = getWordTag(startWordTags[index - 2])
            object.context[0] = preWord2
            object.context[1] = preTag2

        if index < len(startWordTags) - 1:
            nextWord1, nextTag1 = getWordTag(startWordTags[index + 1])
            object.context[6] = nextWord1
            object.context[7] = nextTag1

        if index < len(startWordTags) - 2:
            nextWord2, nextTag2 = getWordTag(startWordTags[index + 2])
            object.context[8] = nextWord2
            object.context[9] = nextTag2

        return object


#    def isSatisfied(self, fwObject):
#        for i in range(13):
#            key = self.context[i]
#            if (key is not None):
#                if key != fwObject.context[i]:
#                    return False
#        return True

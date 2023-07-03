import os


def split_merge_syls(tagged_file="TIB_train_maxmatched.txt.TAGGED"):
    """
    Input: file that is tagged by rdr rules
    Output:
    """
    current_dir = os.path.dirname(__file__)
    relative_path = "../data/" + tagged_file
    file_path = os.path.join(current_dir, relative_path)

    file = open(file_path, encoding="utf-8")
    contents = file.read()
    words_list = contents.split()
    word_tag_list = []
    for word in words_list:
        word_tag_splited = word.split("/")
        word_tag_list.append(word_tag_splited)

    print(word_tag_list)

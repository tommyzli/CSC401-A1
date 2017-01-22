import sys


slang_acronyms = [
    'smh', 'fwb', 'lmfao', 'lmao', 'lms', 'tbh', 'rofl', 'wtf', 'bff', 'wyd', 'lylc',
    'brb', 'atm', 'imao', 'sml', 'btw', 'bw', 'imho', 'fyi', 'ppl', 'sob', 'ttyl',
    'imo', 'ltr', 'thx', 'kk', 'omg', 'ttys', 'afn', 'bbs', 'cya', 'ez', 'f2f', 'gtr',
    'ic', 'jk', 'k', 'ly', 'ya', 'nm', 'np', 'plz', 'ru', 'so', 'tc', 'tmi', 'ym',
    'ur', 'u', 'sol',
]


def feat1():
    '''
    Number of first-person pronouns.
    '''
    pass


def feat2():
    '''
    Number of second-person pronouns.
    '''
    pass


def feat4():
    '''
    Number of third-person pronouns.
    '''
    pass


def feat5():
    '''
    Number of coordinating conjunctions.
    '''
    pass


def feat6():
    '''
    Number of past tense verbs.
    '''
    pass


def feat7():
    '''
    Number of commas.
    '''
    pass


def feat8():
    '''
    Number of colons and semicolons.
    '''
    pass


def feat9():
    '''
    Number of dashes.
    '''
    pass


def feat10():
    '''
    Number of parentheses.
    '''
    pass


def feat11():
    '''
    Number of ellipses.
    '''
    pass


def feat12():
    '''
    Number of common nouns.
    '''
    pass


def feat13():
    '''
    Number of proper nouns.
    '''
    pass


def feat14():
    '''
    Number of adverbs.
    '''
    pass


def feat15():
    '''
    Number of wh-words.
    '''
    pass


def feat16():
    '''
    Number of modern slang acronyms.
    '''
    pass


def feat17():
    '''
    Number of words in all uppercase that are at least 2 characters long.
    '''
    pass


def feat18():
    '''
    Average number of tokens/sentence.
    '''
    pass


def feat19():
    '''
    Average token length (excluding punctuation).
    '''
    pass


def feat20():
    '''
    Number of sentences.
    '''
    pass


if __name__ == '__main__':
    twt_input_path = sys.argv[1]
    output_path = sys.argv[2]
    try:
        num_data_points = sys.argv[3]
    except IndexError:
        num_data_points = None

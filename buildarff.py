import re
import sys


# scan pronoun files for feat1-3
with open('/u/cs401/Wordlists/First-person') as first_person_pronoun_file:
    first_person_pronoun_list = first_person_pronoun_file.read().splitline()

first_person_pronoun_list = [pronoun.lower() for pronoun in first_person_pronoun_list]

with open('/u/cs401/Wordlists/Second-person') as second_person_pronoun_file:
    second_person_pronoun_list = second_person_pronoun_file.read().splitline()

second_person_pronoun_list = [pronoun.lower() for pronoun in second_person_pronoun_list]

with open('/u/cs401/Wordlists/Third-person') as third_person_pronoun_file:
    third_person_pronoun_list = third_person_pronoun_file.read().splitline()

third_person_pronoun_list = [pronoun.lower() for pronoun in third_person_pronoun_list]


slang_acronyms = [
    'smh', 'fwb', 'lmfao', 'lmao', 'lms', 'tbh', 'rofl', 'wtf', 'bff', 'wyd', 'lylc',
    'brb', 'atm', 'imao', 'sml', 'btw', 'bw', 'imho', 'fyi', 'ppl', 'sob', 'ttyl',
    'imo', 'ltr', 'thx', 'kk', 'omg', 'ttys', 'afn', 'bbs', 'cya', 'ez', 'f2f', 'gtr',
    'ic', 'jk', 'k', 'ly', 'ya', 'nm', 'np', 'plz', 'ru', 'so', 'tc', 'tmi', 'ym',
    'ur', 'u', 'sol',
]


def feat1(tweet):
    '''
    Number of first-person pronouns.
    '''
    pass


def feat2(tweet):
    '''
    Number of second-person pronouns.
    '''
    pass


def feat3(tweet):
    '''
    Number of third-person pronouns.
    '''
    pass


def feat4(tweet):
    '''
    Number of coordinating conjunctions.
    '''
    pass


def feat5(tweet):
    '''
    Number of past tense verbs.
    '''
    pass


def feat6(tweet):
    '''
    Number of future tense verbs.
    '''
    pass


def feat7(tweet):
    '''
    Number of commas.
    '''
    pass


def feat8(tweet):
    '''
    Number of colons and semicolons.
    '''
    pass


def feat9(tweet):
    '''
    Number of dashes.
    '''
    pass


def feat10(tweet):
    '''
    Number of parentheses.
    '''
    pass


def feat11(tweet):
    '''
    Number of ellipses.
    '''
    pass


def feat12(tweet):
    '''
    Number of common nouns.
    '''
    pass


def feat13(tweet):
    '''
    Number of proper nouns.
    '''
    pass


def feat14(tweet):
    '''
    Number of adverbs.
    '''
    pass


def feat15(tweet):
    '''
    Number of wh-words.
    '''
    pass


def feat16(tweet):
    '''
    Number of modern slang acronyms.
    '''
    pass


def feat17(tweet):
    '''
    Number of words in all uppercase that are at least 2 characters long.
    '''
    pass


def feat18(tweet):
    '''
    Average number of tokens/sentence.
    '''
    pass


def feat19(tweet):
    '''
    Average token length (excluding punctuation).
    '''
    pass


def feat20(tweet):
    '''
    Number of sentences.
    '''
    pass


def tweet_to_rff(tweet, polarity):
    return '{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18},{19},{20}\n'.format(
        feat1(tweet),
        feat2(tweet),
        feat3(tweet),
        feat4(tweet),
        feat5(tweet),
        feat6(tweet),
        feat7(tweet),
        feat8(tweet),
        feat9(tweet),
        feat10(tweet),
        feat11(tweet),
        feat12(tweet),
        feat13(tweet),
        feat14(tweet),
        feat15(tweet),
        feat16(tweet),
        feat17(tweet),
        feat18(tweet),
        feat19(tweet),
        feat20(tweet),
        polarity,
    )


def main(input_path, output_path, num_data_points):
    num_tweets = 0
    current_tweet = ""
    current_polarity = None
    with open(output_path, 'w') as output_file:
        # TODO first write arff headers

        with open(input_path, 'r') as twt_file:
            for line in twt_file:
                new_tweet = re.search(r'^<A=(\d)>$', line)
                if new_tweet:  # found beginning of a new tweet
                    if current_tweet:
                        output_line = tweet_to_rff(current_tweet, current_polarity)
                        output_file.write(output_line)
                        num_tweets += 1
                    # reset tweet and polarity
                    current_polarity = int(new_tweet.group(1))
                    current_tweet = ""
                else:
                    current_tweet = "{0}{1}".format(current_tweet, line)


if __name__ == '__main__':
    twt_input_path = sys.argv[1]
    output_path = sys.argv[2]
    try:
        num_data_points = sys.argv[3]
        if num_data_points >= 20000:
            num_data_points = None
    except IndexError:
        num_data_points = None

    main(twt_input_path, output_path, num_data_points)

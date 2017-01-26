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
    'smh', 'fwb', 'lmfao', 'lmao', 'lms', 'lol', 'tbh', 'rofl', 'wtf', 'bff', 'wyd',
    'lylc', 'brb', 'atm', 'imao', 'sml', 'btw', 'bw', 'imho', 'fyi', 'ppl', 'sob', 'ttyl',
    'imo', 'ltr', 'thx', 'kk', 'omg', 'ttys', 'afn', 'bbs', 'cya', 'ez', 'f2f', 'gtr',
    'ic', 'jk', 'k', 'ly', 'ya', 'nm', 'np', 'plz', 'ru', 'so', 'tc', 'tmi', 'ym',
    'ur', 'u', 'sol',
]


def get_count(tweet, search_string):
    # words are prefixed by either whitespace or a new line
    return tweet.count(' {}'.format(search_string)) + tweet.count('\n{}'.format(search_string))


def feat1(tweet):
    '''
    Number of first-person pronouns.
    '''
    count = 0
    for pronoun in first_person_pronoun_list:
        count = count + get_count(tweet, pronoun)
    return count


def feat2(tweet):
    '''
    Number of second-person pronouns.
    '''
    count = 0
    for pronoun in second_person_pronoun_list:
        count = count + get_count(tweet, pronoun)
    return count


def feat3(tweet):
    '''
    Number of third-person pronouns.
    '''
    count = 0
    for pronoun in third_person_pronoun_list:
        count = count + get_count(tweet, pronoun)
    return count


def feat4(tweet):
    '''
    Number of coordinating conjunctions.
    '''
    return tweet.count('/CC')


def feat5(tweet):
    '''
    Number of past tense verbs.
    '''
    return tweet.count('/VBD')


def feat6(tweet):
    '''
    Number of future tense verbs.
    '''
    return tweet.count('/VBD')


def feat7(tweet):
    '''
    Number of commas.
    '''
    pass


def feat8(tweet):
    '''
    Number of colons and semicolons.
    '''
    return tweet.count(':') + tweet.count(';')


def feat9(tweet):
    '''
    Number of dashes.
    '''
    return tweet.count('-')


def feat10(tweet):
    '''
    Number of parentheses.
    '''
    return tweet.count('(') + tweet.count(')')


def feat11(tweet):
    '''
    Number of ellipses.
    '''
    return tweet.count('...')


def feat12(tweet):
    '''
    Number of common nouns.
    '''
    # count /NN followed by whitespace so it doesn't collide with /NNS
    return tweet.count('/NN ') + tweet.count('/NN\n') + tweet.count('/NNS')


def feat13(tweet):
    '''
    Number of proper nouns.
    '''
    # count /NNP followed by whitespace so it doesn't collide with /NNPS
    return tweet.count('/NNP ') + tweet.count('/NNP\n') + tweet.count('/NNPS')


def feat14(tweet):
    '''
    Number of adverbs.
    '''
    # count /RB followed by whitespace so it doesn't collide with /RBR or /RBS
    return tweet.count('/RB ') + tweet.count('/RB\n') + tweet.count('/RBR') + tweet.count('/RBS')


def feat15(tweet):
    '''
    Number of wh-words.
    '''
    # count /WP followed by whitespace so it doesn't collide with /WP$
    return tweet.count('/WDT') + tweet.count('/WP$') + tweet.count('/WRB') + tweet.count('/WP ') + tweet.count('/WP\n')


def feat16(tweet):
    '''
    Number of modern slang acronyms.
    '''
    count = 0
    for pronoun in slang_acronyms:
        count = count + get_count(tweet, pronoun)
    return count


def feat17(tweet):
    '''
    Number of words in all uppercase that are at least 2 characters long.
    '''
    return len(re.findall(r'(^|\s)[A-Z]{2,}/', tweet))


def feat18(tweet):
    '''
    Average number of tokens/sentence.
    '''
    if not tweet:
        return 0

    sentences = re.split(r'\n', tweet.lstrip().rstrip())
    tokens_per_sentence = []

    for sentence in sentences:
        split = re.split(r'\s+', sentence)
        tokens_per_sentence.append(len(split))

    return sum(tokens_per_sentence) / len(tokens_per_sentence)


def feat19(tweet):
    '''
    Average token length (excluding punctuation).
    '''
    num_tokens = 0
    token_lengths = []
    tokens = re.split(r'\s+', tweet)
    for token in tokens:
        punctuation_match = re.match(r'^\W/.*', token)
        if punctuation_match:
            # exclude punctuation tokens
            continue

        untagged_token = token.rsplit('/', 1)
        token_lengths.append(len(untagged_token))
        num_tokens = num_tokens + 1

    if not num_tokens:
        return 0

    return sum(token_lengths) / num_tokens


def feat20(tweet):
    '''
    Number of sentences.
    '''
    return len(re.split(r'\n', tweet.lstrip().rstrip()))


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
        output_file.write('@RELATION {}\n\n'.format(output_path))
        output_file.write('@ATTRIBUTE first_person_pronouns NUMERIC\n')
        output_file.write('@ATTRIBUTE second_person_pronouns NUMERIC\n')
        output_file.write('@ATTRIBUTE third_person_pronouns NUMERIC\n')
        output_file.write('@ATTRIBUTE coordinating_conjunctions NUMERIC\n')
        output_file.write('@ATTRIBUTE past_tense_verbs NUMERIC\n')
        output_file.write('@ATTRIBUTE future_tense_verbs NUMERIC\n')
        output_file.write('@ATTRIBUTE commas NUMERIC\n')
        output_file.write('@ATTRIBUTE colons_and_semicolons NUMERIC\n')
        output_file.write('@ATTRIBUTE dashes NUMERIC\n')
        output_file.write('@ATTRIBUTE parentheses NUMERIC\n')
        output_file.write('@ATTRIBUTE ellipses NUMERIC\n')
        output_file.write('@ATTRIBUTE common_nouns  NUMERIC\n')
        output_file.write('@ATTRIBUTE proper_nouns NUMERIC\n')
        output_file.write('@ATTRIBUTE adverbs NUMERIC\n')
        output_file.write('@ATTRIBUTE wh_words NUMERIC\n')
        output_file.write('@ATTRIBUTE slang_acronyms NUMERIC\n')
        output_file.write('@ATTRIBUTE uppercase_words NUMERIC\n')
        output_file.write('@ATTRIBUTE average_length_of_sentences NUMERIC\n')
        output_file.write('@ATTRIBUTE average_length_of_tokens NUMERIC\n')
        output_file.write('@ATTRIBUTE number_of_sentences NUMERIC\n')
        output_file.write('@ATTRIBUTE polarity NUMERIC\n')
        output_file.write('@DATA\n')

        # TODO if num_data_points, limit number of data points

        with open(input_path, 'r') as twt_file:
            for line in twt_file:
                if num_data_points and num_tweets >= num_data_points:
                    # reached max amount to read
                    return

                new_tweet = re.search(r'^<A=(\d)>$', line)

                if new_tweet:
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

import csv
import re
import sys

import NLPlib


tagger = NLPlib.NLPlib()

# get common abbreviations, used for twtt5()
with open('abbrev.english', 'r') as abbreviation_file:
    abbreviation_list = abbreviation_file.read().splitlines()

# add other abbreviations not in the file
abbreviation_list.extend([
    # months
    'jan.', 'feb.', 'mar.', 'apr.', 'jun.', 'aug.', 'sept.', 'oct.', 'nov.', 'dec.',
    # provinces
    'a.b.', 'b.c.', 'm.b.', 'n.b.', 'n.l.', 'n.t.', 'n.s.', 'n.u.', 'o.n.', 'p.e.', 'q.c.', 's.k.', 'y.k.',
    # countries
    'c.a.', 'u.s.', 'u.k.', 'g.b.', 'f.r.', 'c.n.', 'd.e', 'j.p.', 'r.u.',
])

# lowercase all abbreviations
abbreviation_list = [abbrev.lower() for abbrev in abbreviation_list]


HTML_CHARACTER_CODE_MAPPING = {
    '&#32;': ' ',
    '&#33;': '!',
    '&#34;': '"',
    '&#35;': '#',
    '&#36;': '$',
    '&#37;': '%',
    '&#38;': '&',
    '&#39;': '\'',
    '&#40;': '(',
    '&#41;': ')',
    '&#42;': '*',
    '&#43;': '+',
    '&#44;': ',',
    '&#45;': '-',
    '&#46;': '.',
    '&#47;': '/',
    '&#58;': ':',
    '&#59;': ';',
    '&#60;': '<',
    '&#61;': '=',
    '&#62;': '>',
    '&#63;': '?',
    '&#64;': '@',
    '&#91;': '[',
    '&#92;': '\\',
    '&#93;': ']',
    '&#94;': '^',
    '&#95;': '_',
    '&#96;': '`',
    '&#123;': '{',
    '&#124;': '|',
    '&#125;': '}',
    '&#126;': '~',
    '&amp;': '&',
    '&lt;': '<',
    '&gt;': '>',
}


def twtt1(line):
    """
    Remove all html tags from the line.
    """
    return re.sub(r'<[^>]+>', '', line)


def twtt2(line):
    """
    Convert all html character codes to their ascii equivalent.
    """
    for html_code, ascii_value in HTML_CHARACTER_CODE_MAPPING.iteritems():
        if html_code in line:
            line = line.replace(html_code, ascii_value)

    return line


def twtt3(line):
    """
    Remove all URLs from the line.
    """

    # matches (http|www)*.* followed by a single whitespace character or the end of the string
    line = re.sub(r'(http|www)\S+\.\S+(\s{1}|$)', '', line, flags=re.IGNORECASE)

    # short urls
    line = re.sub(r'bit\.ly/\S*(\s|$)', '', line, flags=re.IGNORECASE)
    line = re.sub(r'goo\.gl/\S*(\s|$)', '', line, flags=re.IGNORECASE)
    line = re.sub(r't\.co/\S*(\s|$)', '', line, flags=re.IGNORECASE)
    line = re.sub(r'ow\.ly/\S*(\s|$)', '', line, flags=re.IGNORECASE)
    line = re.sub(r'youtu\.be/\S*(\s|$)', '', line, flags=re.IGNORECASE)

    return line


def twtt4(line):
    """
    Remove all @ and # from the line.
    """
    return re.sub(r'(#|@)(\w*)\b', r'\2', line)


def twtt5(line):
    """
    Add a newline after each sentence.
    """
    indices_to_skip = []

    # first find all indexes of punctuation that should not be split into a new line
    for abbreviation in abbreviation_list:
        if abbreviation not in line.lower():
            continue

        found_index = 0
        offset = 0
        while (found_index != -1 or len(abbreviation) + offset < len(line)):
            found_index = line.lower().find(abbreviation, offset)
            offset += found_index + len(abbreviation)

            # append the index of the punctuation
            if found_index != -1:
                # find local indices of all periods in abbreviation
                # indices_to_skip.append(found_index + len(abbreviation) - 1)
                period_indices = [i for i, char in enumerate(abbreviation) if char == '.']
                indices_to_skip.extend(
                    [found_index + local_index for local_index in period_indices]
                )

    sentence_delimiters = [r'\.', r'!', r'\?']
    indices_of_sentence_delimiters = []
    # find all sentence delimiters that are followed by whitespace
    for delimiter in sentence_delimiters:
        indices_of_sentence_delimiters.extend([
            match.start()
            for match in re.finditer(r'{}\s'.format(delimiter), line)
        ])

    # filter out indexes of abbreviations
    indices_of_sentence_delimiters = [
        index
        for index in indices_of_sentence_delimiters
        if index not in indices_to_skip
    ]

    # turn line into a string to to make modifying elements easier
    line = list(line)
    for index in indices_of_sentence_delimiters:
        line[index + 1] = "\n"

    # turn line back into a string
    return "".join(line)


def twtt7(line):
    """
    Separate each token with spaces (including clitics and punctuation).
    """

    # split punctuation
    line = re.sub(r"([^\w\s']+)", r" \1", line)

    # split clitics
    line = re.sub(r"(\b\w*)('\w*)", r"\1 \2", line)
    return line


def twtt8(line):
    """
    Tag each token with it's part-of-speech.
    """
    line = line.rstrip()
    if not line:
        # skip emty lines
        return line

    whitespace = re.split(r'\S+', line)
    for item in whitespace:
        if len(item) > 2:
            item = item[0]

    split = re.split(r'\s+', line)
    tags = tagger.tag(split)

    newline = ''
    for i in range(0, len(split)):
        newline += '{0}{1}/{2}'.format(whitespace[i], split[i], tags[i])

    return newline


def twtt9(line, polarity):
    """
    Demarcate the tweet.
    """
    return '<A={}>\n'.format(polarity) + line


def process_whole_file(output_file, input_path):
    # run the preprocessors on the entire file
    with open(input_path, 'r') as csv_input:
        reader = csv.reader(csv_input)
        for line in reader:
            polarity = line[0]
            tweet = line[5]

            tweet = twtt1(tweet)
            tweet = twtt2(tweet)
            tweet = twtt3(tweet)
            tweet = twtt4(tweet)
            tweet = twtt5(tweet)
            tweet = twtt7(tweet)
            tweet = twtt8(tweet)
            tweet = twtt9(tweet, polarity)

            if tweet[len(tweet) - 1] != '\n':
                tweet = tweet + '\n'

            output_file.write(tweet)


def process_sections(output_file, input_path, student_id):
    # file is too big, only process 20,000 lines
    base = (student_id % 80) * 10000
    with open(input_path, 'r') as csv_input:
        reader = csv.reader(csv_input)
        for i, line in enumerate(reader):
            if (i >= base and i < base + 10000) or (i >= base + 800000 and i < base + 810000):
                polarity = line[0]
                tweet = line[5]

                tweet = twtt1(tweet)
                tweet = twtt2(tweet)
                tweet = twtt3(tweet)
                tweet = twtt4(tweet)
                tweet = twtt5(tweet)
                tweet = twtt7(tweet)
                tweet = twtt8(tweet)
                tweet = twtt9(tweet, polarity)

                if tweet[len(tweet) - 1] != '\n':
                    tweet = tweet + '\n'

                output_file.write(tweet)


def main(input_path, student_id, output_path):
    # count line numbers in csv input
    line_numbers = sum(1 for line in open(input_path))

    with open(output_path, 'w') as output_file:
        if line_numbers < 1600000:
            process_whole_file(output_file, input_path)
        else:
            process_sections(output_file, input_path, student_id)


if __name__ == '__main__':
    input_path = sys.argv[1]
    student_id = int(sys.argv[2])
    output_path = sys.argv[3]

    main(input_path, student_id, output_path)

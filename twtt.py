import re
import sys


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
    line = re.sub(r'(http|www)\b', '', line)

    # short urls
    line = re.sub(r'bit\.ly/.*', '', line)
    line = re.sub(r'goo\.gl/.*', '', line)
    line = re.sub(r't\.co/.*', '', line)
    line = re.sub(r'ow\.ly/.*', '', line)
    line = re.sub(r'youtu\.be/.*', '', line)

    return line


def twtt4(line):
    """
    Remove all @ and # from the line.
    """
    return re.sub(r'(#|@)(\w*)\b', r'\2', line)


def twtt5(line, abbreviation_list):
    """
    Add a newline after each sentence.
    """
    indices_to_skip = []

    # first find all indexes of punctuation that should not be split into a new line
    for abbreviation in abbreviation_list:
        if abbreviation not in line:
            continue

        found_index = 0
        offset = 0
        while (found_index != -1 or len(abbreviation) + offset < len(line)):
            found_index = line.find(abbreviation, offset)
            offset += found_index + len(abbreviation)

            # append the index of the punctuation
            # (assuming each abbreviation ends with a punctuation symbol)
            if found_index != -1:
                indices_to_skip.append(found_index + len(abbreviation) - 1)

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
    line = re.sub(r"(\b\w+)('\w*')", r'\1 \2', line)
    return line


def twtt8(line):
    """
    Tag each token with it's part-of-speech.
    """
    return line


def twtt9():
    """
    Demarcate the tweet.
    """
    pass


if __name__ == '__main__':
    input_path = sys.argv[1]
    student_id = sys.argv[2]
    output_path = sys.argv[3]

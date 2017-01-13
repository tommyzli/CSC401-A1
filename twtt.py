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
    return re.sub(r'(http|www)\b', '', line)


def twtt4(line):
    """
    Remove all @ and # from the line.
    """
    return re.sub(r'(#|@)(\w*)\b', r'\2', line)


def twtt5():
    """
    Add a newline after each sentence.
    """
    pass


def twtt7():
    """
    Separate each token with spaces (including clitics and punctuation).
    """
    pass


def twtt8():
    """
    Tag each token with it's part-of-speech.
    """
    pass


def twtt9():
    """
    Demarcate the tweet.
    """
    pass


if __name__ == '__main__':
    input_path = sys.argv[1]
    student_id = sys.argv[2]
    output_path = sys.argv[3]

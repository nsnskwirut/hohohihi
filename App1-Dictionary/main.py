import json
from difflib import get_close_matches as gcm


def open_json_file(path_to_file):
    with open(path_to_file, 'r') as data:
        return json.load(data)


def beauty_out(list_of_defin, appendix=''):
    for i, item in enumerate(list_of_defin):
        print "{}{}: {}".format(appendix, i+1, item)


def translate(dict_keyword):
    dict_keyword = dict_keyword.lower()
    vocab_content = open_json_file('data.json')
    possibilities = gcm(dict_keyword, vocab_content.keys(), 6, 0.7)

    if dict_keyword in vocab_content:
        beauty_out(vocab_content[dict_keyword], '  def.')
    elif dict_keyword.title() in vocab_content:
        beauty_out(vocab_content[dict_keyword.title()], '  def.')
    elif dict_keyword.upper() in vocab_content:
        beauty_out(vocab_content[dict_keyword.upper()], '  def.')
    elif len(possibilities) > 0:
        while 0 < 1:
            try:
                print("\nYour word has not been found. Did you mean...")
                beauty_out(possibilities, '   ')
                corrected_ans = input("\nDid you mean any of these? Enter number {}-{} to choose "
                                      "a proper word: ".format(1, len(possibilities)))
            except (SyntaxError, NameError):
                print('Only number input is allowed in submenu.')
            else:
                try:
                    dict_keyword = possibilities[corrected_ans - 1]
                except IndexError:
                    print("Number out of range passed. Enter again: ")
                else:
                    print("\nChosen word: {}".format(dict_keyword.upper()))
                    beauty_out(vocab_content[dict_keyword], '  def.')
                    break
    else:
        print "The word doesn't exist. Please, double check it."


if __name__ == '__main__':
    searched_word = raw_input("Enter word: ")
    translate(searched_word)

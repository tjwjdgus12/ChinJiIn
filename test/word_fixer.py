import cheonjiin_convert as cji_converter
import deletes_convert as del_converter

def load_dict():
    dicts = dict()
    with open("dict_cheonjiin_del.txt", 'r', encoding='utf-8') as dict_del_file:
        for line in dict_del_file:
            line = line[:-1]
            words = line.split('&')
            dicts[words[0]] = words[1:]
    return dicts

dicts = load_dict()

def fix(input_word):
    global dicts

    input_word = cji_converter.cheonjiin_convert(input_word)

    if input_word in dicts.keys():
        return input_word, "correct"

    for dic in dicts.keys():
        if input_word in dicts[dic]:
            return dic, "typo - deletion"

    for input_word_del in del_converter.deletes(input_word):
        if input_word_del in dicts.keys():
            return input_word_del, "typo - insertion"

    for input_word_del in del_converter.deletes(input_word):
        for dic in dicts.keys():
            if input_word_del in dicts[dic]:
                return dic, "typo - etc"

    return input_word, "???"

def check(input_word):
    fixed, msg = fix(input_word)
    print(fixed, msg)

while True:
    inp = input()
    check(inp)

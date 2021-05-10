import cheonjiin_convert as cji_converter
import deletes_convert as del_converter
import hangeul_convert as han_converter

def load_dict():
    dicts = dict()
    with open("dict_cheonjiin_del.txt", 'r', encoding='utf-8') as dict_del_file:
        for line in dict_del_file:
            line = line[:-1]
            words = line.split('&')
            dicts[words[0]] = words[1:]
    return dicts


dicts = load_dict()
print("dictionary loaded.")

def fix(input_word):
    global dicts

    input_word = cji_converter.cheonjiin_convert(input_word)

    ret = set()

    if input_word in dicts.keys():
        ret.add(han_converter.hangeul_convert(input_word))

    for dic in dicts.keys():
        if input_word in dicts[dic]:
            ret.add(han_converter.hangeul_convert(dic))

    for input_word_del in del_converter.deletes(input_word):
        if input_word_del in dicts.keys():
            ret.add(han_converter.hangeul_convert(input_word_del))

    for input_word_del in del_converter.deletes(input_word):
        for dic in dicts.keys():
            if input_word_del in dicts[dic]:
                ret.add(han_converter.hangeul_convert(dic))

    for r in ret:
        print(r)
    print("------------------")

while True:
    fix(input())

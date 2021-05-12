import cheonjiin_convert as cji_converter
import deletes_convert as del_converter
import hangeul_convert as han_converter


def load_delete_dict(inputFile):
    _delete_dicts = dict()
    with open(inputFile, 'rt', encoding='utf-8') as dict_del_file:
        for line in dict_del_file:
            line = line[:-1]
            words = line.split('&')
            _delete_dicts[words[0]] = words[1:]
    print("delete dictionary file loaded")
    return _delete_dicts


def load_origin_dict(inputFile):
    _origin_dict = dict()
    with open(inputFile, 'r') as file_dict:
        for line in file_dict:
            temp = line.split()
            _origin_dict[temp[0].strip(':')] = int(temp[1])
    print("original dictionary file loaded")
    return _origin_dict


def fix(input_word):
    global delete_dict
    global origin_dict

    origin_input = input_word
    input_word = cji_converter.cheonjiin_convert(input_word)

    ret = set()

    if input_word in delete_dict.keys():
        ret.add(han_converter.hangeul_convert(input_word))

    for dic in delete_dict.keys():
        if input_word in delete_dict[dic]:
            ret.add(han_converter.hangeul_convert(dic))

    for input_word_del in del_converter.deletes(input_word):
        if input_word_del in delete_dict.keys():
            ret.add(han_converter.hangeul_convert(input_word_del))

    for input_word_del in del_converter.deletes(input_word):
        for dic in delete_dict.keys():
            if input_word_del in delete_dict[dic]:
                ret.add(han_converter.hangeul_convert(dic))

    print_arr = []
    hasSame = False
    for i in ret:
        if i in origin_dict.keys():
            if i == origin_input:
                hasSame = True
                continue
            else:
                temp = [i, origin_dict[i]]
        else:
            temp = [i, int(0)]
        print_arr.append(temp)
    print_arr.sort(key=lambda freq: freq[1], reverse=True)
    if hasSame == True:
        print_arr.insert(0, [origin_input, origin_dict[origin_input]])

    for r in print_arr:
        print(r[0])
    print("------------------")


if __name__ == '__main__':
    dictionaryFileName = "dict.txt"
    origin_dict = load_origin_dict(dictionaryFileName)

    deleteDictFileName = "dict_del.txt"
    del_converter.createDeleteDict(dictionaryFileName, deleteDictFileName)
    delete_dict = load_delete_dict(deleteDictFileName)
    print("단어를 입력해주세요.")
    while True:
        fix(input())

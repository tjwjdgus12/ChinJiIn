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
origin_dict = dict()
with open('dict.txt', 'r') as file_dict:
    for line in file_dict:
        temp = line.split()
        origin_dict[temp[0].strip(':')] = int(temp[1])
print("dictionary loaded.")

def fix(input_word):
    global dicts
    global origin_dict

    origin_input = input_word
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
    print_arr.sort(key = lambda freq: freq[1], reverse=True)
    if hasSame == True:
        print_arr.insert(0, [origin_input, origin_dict[origin_input]])
    
    for r in print_arr:
        print(r[0])
    print("------------------")

while True:
    fix(input())

import cheonjiin_convert as cji_converter
import deletes_convert as del_converter
import hangeul_convert as han_converter


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
    global cji_dict
    
    origin_input = input_word
    input_word = cji_converter.cheonjiin_convert(input_word)

    ret = set()

    if input_word in cji_dict.keys():
        ret.add(han_converter.hangeul_convert(input_word))
        print('단어사전에 입력 키워드가 있는 예시', input_word)

    if input_word in delete_dict.keys():
        for keyword in delete_dict[input_word]:
            ret.add(han_converter.hangeul_convert(keyword))
            print('단어사전 del에 입력 키워드가 있는 예시', keyword)

    for input_word_del in del_converter.deletes(input_word):
        if input_word_del in cji_dict.keys():
            ret.add(han_converter.hangeul_convert(input_word_del))
            print('단어사전에 입력 키워드 del가 있는 예시', input_word_del)

    for input_word_del in del_converter.deletes(input_word):
        if input_word_del in delete_dict.keys():
            for keyword in delete_dict[input_word_del]:
                ret.add(han_converter.hangeul_convert(keyword))
                print('단어사전 del에 입력 키워드 del가 있는 예시', keyword)

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
    if hasSame:
        print_arr.insert(0, [origin_input, origin_dict[origin_input]])

    for r in print_arr:
        print(r[0])
    print("------------------")


if __name__ == '__main__':
    dictionaryFileName = "dict.txt"
    origin_dict = load_origin_dict(dictionaryFileName)
    cji_dict = cji_converter.load_cji_dict(dictionaryFileName)
    delete_dict = del_converter.makeDeleteDict(dictionaryFileName)

    print("단어를 입력해주세요.")
    while True:
        fix(input())



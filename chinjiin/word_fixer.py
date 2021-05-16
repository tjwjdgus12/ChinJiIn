from converter import cji_converter, del_converter, han_converter
from measurer import edit_distance_calculater

DICTIONARY = 'mungchi_dict'

def fix(input_word):
    global del_dict, cji_dict
    
    input_word = cji_converter.convert(input_word)

    ret = set()

    if input_word in cji_dict.keys():
        ret.add(input_word)
        print('단어사전에 입력 키워드가 있는 예시', input_word)

    if input_word in del_dict.keys():
        for keyword in del_dict[input_word]:
            ret.add(keyword)
            print('단어사전 del에 입력 키워드가 있는 예시', keyword)

    for input_word_del in del_converter.deletes(input_word):
        if input_word_del in cji_dict.keys():
            ret.add(input_word_del)
            print('단어사전에 입력 키워드 del가 있는 예시', input_word_del)

    for input_word_del in del_converter.deletes(input_word):
        if input_word_del in del_dict.keys():
            for keyword in del_dict[input_word_del]:
                ret.add(keyword)
                print('단어사전 del에 입력 키워드 del가 있는 예시', keyword)

    print_arr = []
    has_same = False
    for i in ret:
        if i in cji_dict:
            if i == input_word:
                has_same = True
                continue
            else:
                temp = [i, cji_dict[i]]
        else:
            temp = [i, int(0)]
        print_arr.append(temp)
    print_arr.sort(key=lambda freq: freq[1], reverse=True)
    if has_same:
        print_arr.insert(0, [input_word, cji_dict[input_word]])

    for r in print_arr:
        print('교정단어: %s' % han_converter.convert(r[0]), end = ' ')
        edit_dist = edit_distance_calculater.calc_edit_dist(input_word, r[0])
        print('편집거리: %.2f' % edit_dist, end = ' ')
        print('빈도수: ', r[1])
    print("------------------")


if __name__ == '__main__':
    cji_converter.make_file(DICTIONARY, reset = True)
    
    cji_dict = cji_converter.load_cji_dict(DICTIONARY)
    del_dict = del_converter.load_del_dict(DICTIONARY)
 
    while True:
        print("Input:", end = ' ')
        fix(input())

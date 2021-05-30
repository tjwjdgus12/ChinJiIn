from converter import cji_converter, del_converter, han_converter
from measurer import edit_distance_calculater

DICTIONARY = 'mungchi_dict'
RESET_ON_EVERY_EXECUTION = False


def fix(input_word):
    input_word = cji_converter.convert(input_word)
    candidates = get_candidates(input_word)
    print_candidates(sorted_candidates(input_word, candidates))


def get_candidates(input_word):
    ret = set()
    
    if input_word in cji_dict.keys():
        ret.add(input_word)
        #print('단어사전에 입력 키워드가 있는 예시', input_word)

    if input_word in del_dict.keys():
        for keyword in del_dict[input_word]:
            ret.add(keyword)
            #print('단어사전 del에 입력 키워드가 있는 예시', keyword)

    for input_word_del in del_converter.deletes(input_word):
        if input_word_del in cji_dict.keys():
            ret.add(input_word_del)
            #print('단어사전에 입력 키워드 del가 있는 예시', input_word_del)

    for input_word_del in del_converter.deletes(input_word):
        if input_word_del in del_dict.keys():
            for keyword in del_dict[input_word_del]:
                ret.add(keyword)
                #print('단어사전 del에 입력 키워드 del가 있는 예시', keyword)

    return ret


def sorted_candidates(input_word, candidates):
    print_arr = []
    
    for cand in candidates:
        temp = [
            cand,
            1 - (cji_dict[cand] / 54868),
            edit_distance_calculater.calc_edit_dist(input_word, cand)
        ]
        print_arr.append(temp)
        
    print_arr.sort(key = lambda freq: (freq[1] / 2) + freq[2])
    return print_arr


def print_candidates(candidates):
    for cand in candidates:
        print('교정단어: %s' % han_converter.convert(cand[0]), end = ' ')
        print('물리적 편집거리: %.2f' % cand[2], end = ' ')
        print('정규화된 빈도수: %.6f' % cand[1])
    print("------------------")


if __name__ == '__main__':
    cji_converter.make_file(DICTIONARY, RESET_ON_EVERY_EXECUTION)
    
    cji_dict = cji_converter.load_cji_dict(DICTIONARY)
    del_dict = del_converter.load_del_dict(DICTIONARY)
 
    while True:
        fix(input("Input: "))

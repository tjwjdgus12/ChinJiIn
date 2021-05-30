from converter import cji_converter, del_converter, han_converter
from measurer import edit_distance_calculater
from datetime import timedelta
from timeit import default_timer as timer

DICTIONARY = 'optimized_dict'
RESET_ON_EVERY_EXECUTION = False


def fix(input_word):
    input_word = cji_converter.convert(input_word)
    
    search_start_time = timer()
    candidates = get_candidates(input_word)
    search_end_time = timer()
    print('탐색 소요 시간 : ' + str(timedelta(seconds=search_end_time - search_start_time)))
    
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

    if not ret:
        print('입력한 \'' + han_converter.convert(input_word) + ', ' + input_word + '\' 는 교정 단어 목록이 존재하지 않습니다.')
        print("------------------")
        return

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
    del_converter.make_file(DICTIONARY, RESET_ON_EVERY_EXECUTION)
    
    cji_dict = cji_converter.load_cji_dict(DICTIONARY)
    del_dict = del_converter.load_del_dict_by_file(DICTIONARY)
 
    while True:
        fix(input("Input: "))

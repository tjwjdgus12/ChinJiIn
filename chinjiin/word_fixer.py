from converter import cji_converter, del_converter, han_converter
from measurer import edit_distance_calculater
from datetime import timedelta
from timeit import default_timer as timer

DICTIONARY = 'mungchi_dict'
RESET_ON_EVERY_EXECUTION = False


def fix(input_word):
    global del_dict, cji_dict
    input_word = cji_converter.convert(input_word)
    resCnt = 0
    ret = set()
    search_start_time = timer()
    if input_word in cji_dict.keys():
        ret.add(input_word)
        print('단어사전에 입력 키워드가 있는 예시', input_word)
        resCnt += 1

    if input_word in del_dict.keys():
        for keyword in del_dict[input_word]:
            if keyword in ret:
                continue
            ret.add(keyword)
            print('단어사전 del에 입력 키워드가 있는 예시', keyword)
            resCnt += 1

    for input_word_del in del_converter.deletes(input_word):
        if input_word_del in cji_dict.keys():
            if input_word_del in ret:
                continue
            ret.add(input_word_del)
            print('단어사전에 입력 키워드 del가 있는 예시', input_word_del)
            resCnt += 1

    for input_word_del in del_converter.deletes(input_word):
        if input_word_del in del_dict.keys():
            for keyword in del_dict[input_word_del]:
                if keyword in ret:
                    continue
                ret.add(keyword)
                print('단어사전 del에 입력 키워드 del가 있는 예시', keyword)
                resCnt += 1

    if not resCnt:
        print('입력한 \'' + han_converter.convert(input_word) + ', ' + input_word + '\' 는 교정 단어 목록이 존재하지 않습니다.')
        print("------------------")
        return

    print_arr = []
    has_same = False
    for i in ret:
        if i in cji_dict:
            if i == input_word:
                has_same = True
                continue
            else:
                temp = [i, 1 - (cji_dict[i] / 54868), edit_distance_calculater.calc_edit_dist(input_word, i)]
        else:
            temp = [i, int(1), edit_distance_calculater.calc_edit_dist(input_word, i)]
        print_arr.append(temp)
    print_arr.sort(key=lambda freq: (freq[1] / 2) + freq[2])
    
    if has_same:
        print_arr.insert(0, [input_word, (1 - cji_dict[input_word] / 54868), 0])

    search_end_time = timer()
    print('탐색 소요 시간 : ' + str(timedelta(seconds=search_end_time - search_start_time)))
    for r in print_arr:
        print('교정단어: %s' % han_converter.convert(r[0]), end=' ')
        print('물리적 편집거리: %.2f' % r[2], end=' ')
        print('정규화된 빈도수: ', r[1])
    print("------------------")


if __name__ == '__main__':
    cji_converter.make_file(DICTIONARY, RESET_ON_EVERY_EXECUTION)
    
    cji_dict = cji_converter.load_cji_dict(DICTIONARY)
    del_dict = del_converter.load_del_dict(DICTIONARY)
 
    while True:
        print("Input:", end = ' ')
        fix(input())

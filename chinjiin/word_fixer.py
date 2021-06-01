from datetime import timedelta
from converter import cji_converter, del_converter, han_converter
from measurer import edit_distance_calculater
from timeit import default_timer as timer

DICTIONARY = 'optimized_dict'
MAX_FREQ = 54868


def load_dict(): # It must be called before fix
    global cji_dict, del_dict
    cji_dict = cji_converter.load_cji_dict(DICTIONARY)
    del_dict = del_converter.load_del_dict_by_file(DICTIONARY)


def direct_fix(input_word):
    input_word_cji = cji_converter.convert(input_word)
    candidates = get_candidates(input_word_cji)
    if candidates:
        return han_converter.convert(
            min(candidates, key = lambda k: sort_key(k, input_word_cji)))
    else:
        return input_word


def direct_bigram_fix(input_word):
    input_word_cji = cji_converter.convert(input_word)
    candidates = get_candidates(input_word_cji, tuple_with_key=True)

    for i in range(1, len(input_word)):
        left = cji_converter.convert(input_word[:i])
        left_candidates = get_candidates(left, tuple_with_key=True)
        if not left_candidates:
            continue
        fixed_left = min(left_candidates, key = lambda k: k[1])
        
        right = cji_converter.convert(input_word[i:])
        right_candidates = get_candidates(right, tuple_with_key=True)
        if not right_candidates:
            continue
        fixed_right = min(right_candidates, key = lambda k: k[1])

        fixed_word = fixed_left[0] + '#' + fixed_right[0]
        edit_dist = fixed_left[1] + fixed_right[1] + 1 # penalty
        candidates.append((fixed_word, edit_dist))

    if candidates:
        return han_converter.convert(
            min(candidates, key = lambda k: k[1])[0])
    else:
        return input_word


def test_bigram_fix(input_word):
    search_start_time = timer()
    input_word_cji = cji_converter.convert(input_word)
    candidates = get_candidates(input_word_cji, tuple_with_key=True)

    for i in range(1, len(input_word)):
        left = cji_converter.convert(input_word[:i])
        left_candidates = get_candidates(left, tuple_with_key=True)
        if not left_candidates:
            continue
        fixed_left = min(left_candidates, key = lambda k: k[1])
        
        right = cji_converter.convert(input_word[i:])
        right_candidates = get_candidates(right, tuple_with_key=True)
        if not right_candidates:
            continue
        fixed_right = min(right_candidates, key = lambda k: k[1])

        if fixed_left[0][-1] == fixed_right[0][0] and\
            fixed_left[0][-1] in ['ㄱ', 'ㄴ', 'ㄷ', 'ㅇ', 'ㅂ', 'ㅅ', 'ㅈ']:
                fixed_word = fixed_left[0] + '#' + fixed_right[0]
        else:
            fixed_word = fixed_left[0] + fixed_right[0]
        edit_dist = fixed_left[1] + fixed_right[1] + 1 # penalty
        
        if fixed_word not in [cand[0] for cand in candidates]:
            candidates.append((fixed_word, edit_dist))

    candidates.sort(key=lambda k: k[1])
    search_end_time = timer()
    print()

    for cand in candidates:
        print('교정단어: %s' % han_converter.convert(cand[0]))
        print('정렬키: %.6f\n' % cand[1])
    print('단어 교정 시간 : %s s\n' % str(timedelta(seconds=search_end_time - search_start_time)))
    print('--------------------------------------------\n')
    

def test_fix(input_word):
    input_word = cji_converter.convert(input_word)
    candidates = get_candidates(input_word)
    if not candidates:
        print('입력한 \'' + han_converter.convert(input_word) + ', ' + input_word + '\' 는 교정 단어 목록이 존재하지 않습니다.')
        print("------------------")
        return
    candidates.sort(key = lambda k: sort_key(k, input_word)) 
    for cand in candidates:
        print('교정단어: %s' % han_converter.convert(cand))
        key = sort_key(cand, input_word)
        freq = cji_dict[cand]
        edit_dist = edit_distance_calculater.calc_edit_dist(input_word, cand)
        print('\t정렬키: %.6f' % key)
        print('\t편집거리: %.2f' % edit_dist)
        print('\t빈도수: %d\n' % freq)


def get_candidates(input_word, tuple_with_key=False):
    candidates = set()
    
    if input_word in cji_dict.keys():
        candidates.add(input_word)
        #print('단어사전에 입력 키워드가 있는 예시', input_word)

    if input_word in del_dict.keys():
        for keyword in del_dict[input_word]:
            candidates.add(keyword)
            #print('단어사전 del에 입력 키워드가 있는 예시', keyword)

    for input_word_del in del_converter.deletes(input_word):
        if input_word_del in cji_dict.keys():
            candidates.add(input_word_del)
            #print('단어사전에 입력 키워드 del가 있는 예시', input_word_del)

    for input_word_del in del_converter.deletes(input_word):
        if input_word_del in del_dict.keys():
            for keyword in del_dict[input_word_del]:
                candidates.add(keyword)
                #print('단어사전 del에 입력 키워드 del가 있는 예시', keyword)

    if tuple_with_key:
        return [(cand, sort_key(cand, input_word)) for cand in candidates]
    else:
        return list(candidates)
    

def sort_key(candidate, input_word):
    normalized_freq = (1 - cji_dict[candidate]/MAX_FREQ) / 2
    edit_dist = edit_distance_calculater.calc_edit_dist(input_word, candidate)
    
    return normalized_freq + edit_dist



if __name__ == '__main__':
    dictload_start_time = timer()
    load_dict()
    dictload_end_time = timer()
    print('사전 로딩 시간 : %s s\n' % str(timedelta(seconds=dictload_end_time-dictload_start_time)))
    print('--------------------------------------------\n')
 
    while True:
        test_bigram_fix(input("Input: "))

else:
    load_dict()

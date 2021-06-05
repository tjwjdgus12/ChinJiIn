import re
from datetime import timedelta
from converter import cji_converter, del_converter, han_converter
from measurer import edit_distance_calculater
from timeit import default_timer as timer

DICTIONARY = 'optimized_dict'
MAX_FREQ = 54868


def load_dict(filename=DICTIONARY):  # It must be called before fix
    global cji_dict, del_dict
    cji_dict = cji_converter.load_cji_dict(filename)
    del_dict = del_converter.load_del_dict_by_file(filename)


def no_any_han(word):
    p = re.compile('[ㄱ-ㅎㅏ-ㅣ가-힣]')
    return not bool(p.search(word))


def only_han(word):
    p = re.compile('[ㄱ-ㅎㅏ-ㅣ가-힣]+')
    return bool(p.match(word))


def direct_fix(input_word):
    input_word_cji = cji_converter.convert(input_word)
    candidates = get_candidates(input_word_cji)

    for i in range(1, len(input_word)):
        left = cji_converter.convert(input_word[:i])
        left_candidates = get_candidates(left)
        if not left_candidates:
            continue
        fixed_left = min(left_candidates, key=lambda k: k[1])

        right = cji_converter.convert(input_word[i:])
        right_candidates = get_candidates(right)
        if not right_candidates:
            continue
        fixed_right = min(right_candidates, key=lambda k: k[1])

        fixed_word = fixed_left[0] + '#' + fixed_right[0]
        edit_dist = fixed_left[1] + fixed_right[1] + 1  # penalty
        candidates.append((fixed_word, edit_dist))

    if candidates:
        return han_converter.convert(
            min(candidates, key=lambda k: k[1])[0])
    else:
        return input_word


def more_fix(input_word, info=False):
    input_word_cji = cji_converter.convert(input_word)
    candidates = get_candidates(input_word_cji)

    for i in range(1, len(input_word)):
        left = cji_converter.convert(input_word[:i])
        left_candidates = get_candidates(left)
        if not left_candidates:
            continue
        fixed_left = min(left_candidates, key=lambda k: k[1])

        right = cji_converter.convert(input_word[i:])
        right_candidates = get_candidates(right)
        if not right_candidates:
            continue
        fixed_right = min(right_candidates, key=lambda k: k[1])

        if fixed_left[0][-1] == fixed_right[0][0] and \
                fixed_left[0][-1] in ['ㄱ', 'ㄴ', 'ㄷ', 'ㅇ', 'ㅂ', 'ㅅ', 'ㅈ']:
            fixed_word = fixed_left[0] + '#' + fixed_right[0]
        else:
            fixed_word = fixed_left[0] + fixed_right[0]
        edit_dist = fixed_left[1] + fixed_right[1] + 1  # penalty

        if fixed_word not in [cand[0] for cand in candidates]:
            candidates.append((fixed_word, edit_dist))

    candidates.sort(key=lambda k: k[1])
    
    if info:
        return candidates
    else:
        return [han_converter.convert(cand[0]) for cand in candidates]


def debug_fix(input_word):
    search_start_time = timer()
    candidates = more_fix(input_word, info=True)
    search_end_time = timer()

    print()
    for cand in candidates:
        print('교정단어: %s' % han_converter.convert(cand[0]))
        print('정렬키: %.6f\n' % cand[1])
    print('단어 교정 시간 : %s s\n' % str(timedelta(seconds=search_end_time - search_start_time)))
    print('--------------------------------------------\n')


def get_candidates(input_word):
    if no_any_han(input_word):
        return [(input_word, 0)]
    if not only_han(input_word):
        return []

    candidates = set()

    if input_word in cji_dict.keys():
        candidates.add(input_word)
        # print('단어사전에 입력 키워드가 있는 예시', input_word)

    if input_word in del_dict.keys():
        for keyword in del_dict[input_word]:
            candidates.add(keyword)
            # print('단어사전 del에 입력 키워드가 있는 예시', keyword)

    for input_word_del in del_converter.deletes(input_word):
        if input_word_del in cji_dict.keys():
            candidates.add(input_word_del)
            # print('단어사전에 입력 키워드 del가 있는 예시', input_word_del)

    for input_word_del in del_converter.deletes(input_word):
        if input_word_del in del_dict.keys():
            for keyword in del_dict[input_word_del]:
                candidates.add(keyword)
                # print('단어사전 del에 입력 키워드 del가 있는 예시', keyword)

    return [(cand, sort_key(cand, input_word)) for cand in candidates]


def sort_key(candidate, input_word):
    normalized_freq = (1 - cji_dict[candidate] / MAX_FREQ) / 2
    edit_dist = edit_distance_calculater.calc_edit_dist(candidate, input_word)

    return normalized_freq + edit_dist


if __name__ == '__main__':
    dictload_start_time = timer()
    load_dict()
    dictload_end_time = timer()
    print('사전 로딩 시간 : %s s\n' % str(timedelta(seconds=dictload_end_time - dictload_start_time)))
    print('--------------------------------------------\n')

    while True:
        debug_fix(input("Input: "))

else:
    load_dict()

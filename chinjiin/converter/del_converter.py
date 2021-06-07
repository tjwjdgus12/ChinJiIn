import os
import pickle

DICT_PATH = 'converter/dict/'


def deletes(word):
    cycle = (('ㅇ', 'ㄴ'),
             ('ㄱ', 'ㅂ', 'ㅈ', 'ㄷ', 'ㅅ'))
    dels = list()

    for i in range(len(word)):
        flag = False
        if word[i] == '#' and word[i - 1] == word[i + 1]:
            for c in range(2):
                cnt = 2
                ll = i - 2
                rr = i + 2
                if word[i - 1] in cycle[c]:
                    while cnt < c + 3:
                        if ll < 0 or word[ll] != word[i - 1]:
                            break
                        cnt += 1
                        ll -= 1
                    while cnt < c + 3:
                        if rr >= len(word) or word[rr] != word[i - 1]:
                            break
                        cnt += 1
                        rr += 1
                if cnt >= c + 3:
                    dels.append(word[:ll + 2] + word[rr:])
                    flag = True

        if not flag:
            ll = i
            rr = i + 1
            if 2 <= i <= len(word)-3:
                if word[i-1] == '#' and word[i-2] == word[i] \
                   and word[i] in cycle[0] + cycle[1]:
                    ll = i - 1
                elif word[i+1] == '#' and word[i+2] == word[i] \
                     and word[i] in cycle[0] + cycle[1]:
                    rr = i + 2
            dels.append(word[:ll] + word[rr:])

    return dels


def load_del_dict(dict_name):
    del_dict = dict()
    cji_dict_file = 'converter/dict/%s_cji.txt' % dict_name
    with open(cji_dict_file, 'rt', encoding='utf-8') as rf:
        for word in rf:
            word = word.split(':')[0]
            for d in deletes(word):
                if d in del_dict:
                    if word in del_dict[d]:
                        continue
                    del_dict[d].append(word)
                else:
                    del_dict[d] = list()
                    del_dict[d].append(word)

    print("delete dictionary loaded")
    return del_dict


def make_file(dict_name):
    origin_dict_file = DICT_PATH + '%s.txt' % dict_name
    del_dict_file = DICT_PATH + '%s_del.pickle' % dict_name
    del_dict = load_del_dict(dict_name)
    with open(del_dict_file, 'wb') as f:
        pickle.dump(del_dict, f, pickle.HIGHEST_PROTOCOL)


def load_del_dict_by_file(dict_name, reset=False):
    del_dict_file = DICT_PATH + '%s_del.pickle' % dict_name
    if not os.path.isfile(del_dict_file) or reset:
        make_file(dict_name)
    with open(del_dict_file, 'rb') as f:
        data = pickle.load(f)
    print("delete dictionary loaded")
    return data


if __name__ == '__main__':
    DICT_PATH = 'dict/'

from collections import defaultdict
from pathlib import Path

DICT_PATH = Path(__file__).resolve().parent / 'dict'


def deletes(word):
    cycle = (('ㅇ', 'ㄴ'),
             ('ㄱ', 'ㅂ', 'ㅈ', 'ㄷ', 'ㅅ'))
    dels = list()

    for i in range(len(word)):
        flag = False
        if (word[i] == '#' and 0 < i < len(word) - 1
                and word[i - 1] == word[i + 1]):
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
                if word[i-1] == '#' and word[i] in cycle[0] + cycle[1]:
                    if word[i-2] == word[i]:
                        ll = i - 1
                    elif word[i+2] == word[i]:
                        rr = i + 2
            dels.append(word[:ll] + word[rr:])

    return dels


def build_delete_index(words):
    delete_index = defaultdict(set)
    for word in words:
        for deleted in deletes(word):
            delete_index[deleted].add(word)
    return dict(delete_index)


def load_del_dict(dict_name):
    cji_dict_file = DICT_PATH / ('%s_cji.txt' % dict_name)
    words = set()
    with open(cji_dict_file, 'rt', encoding='utf-8') as rf:
        for line in rf:
            words.add(line.rsplit(': ', 1)[0])
    return build_delete_index(words)


def make_file(dict_name):
    """Build and return an in-memory delete index.

    Kept for compatibility with the previous public helper. The project no
    longer writes pickle files into the installed package directory.
    """
    return load_del_dict(dict_name)


def load_del_dict_by_file(dict_name, reset=False):
    """Return a freshly built delete index without loading unsafe pickle data."""
    return load_del_dict(dict_name)


if __name__ == '__main__':
    pass

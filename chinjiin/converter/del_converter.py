import os
import pickle

def deletes(word):
    dels = []
    cycle = [['ㅇ','ㄴ'], ['ㄱ','ㅂ','ㅈ','ㄷ','ㅅ']]
    for i in range(len(word)):
        # 공백이 지워질 경우 연속 자음 축약
        flag = False
        if word[i] == '#' and word[i-1] == word[i+1]:
            for c in range(2):
                cnt = 2
                l = i - 2
                r = i + 2
                if word[i-1] in cycle[c]:
                    while cnt < c + 3:
                        if l < 0 or word[l] != word[i-1]:
                            break
                        cnt += 1
                        l -= 1
                    while cnt < c + 3:
                        if r >= len(word) or word[r] != word[i-1]:
                            break
                        cnt += 1
                        r += 1
                if cnt >= c + 3:
                    dels.append(word[:l+2] + word[r:])
                    flag = True            
        if not flag:
            dels.append(word[:i] + word[i+1:])
            
    return dels


def load_del_dict(dict_name):  # dict.txt 입력받아서 바로 딕셔너리 리턴
    del_dict = dict()
    cji_dict_file = 'converter/dict/%s_cji.txt'%(dict_name)
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
    origin_dict_file = 'converter/dict/%s.txt'%(dict_name)
    del_dict_file = 'converter/dict/%s_del.pickle'%(dict_name)
    if not os.path.isfile(del_dict_file) or reset:
        del_dict = load_del_dict(dict_name)
        with open(del_dict_file, 'wb') as f:
            pickle.dump(del_dict, f, pickle.HIGHEST_PROTOCOL)


def load_del_dict_by_file(dict_name):
    del_dict_file = 'converter/dict/%s_del.pickle'%(dict_name)
    with open(del_dict_file, 'rb') as f:
        data = pickle.load(f)    


if __name__ == '__main__':
    pass

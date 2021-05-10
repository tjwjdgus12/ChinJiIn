def deletes(word):
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [L + R[1:] for L, R in splits if R]
    return deletes

def make_output(inputfile, outputfile):
    wf = open(outputfile, 'w',encoding='utf-8')
    with open(inputfile, 'r', encoding='utf-8') as rf:
        for word in rf:
            line = []
            line.append(word[:-1]) # 개행 제거
            for d in deletes(word[:-1]):
                line.append(d)
            wf.write('&'.join(line) + '\n')
    wf.close()

make_output("dict_cheonjiin.txt", "dict_cheonjiin_del.txt")

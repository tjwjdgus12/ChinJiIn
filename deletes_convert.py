import cheonjiin_convert as cji_convert
import os

def deletes(word):
    dels = []
    cycle = [['ㅇ','ㄴ'], ['ㄱ','ㅂ','ㅈ','ㄷ','ㅅ']]
    for i in range(len(word)):
        if word[i] == '#' and word[i-1] == word[i+1]:
            cnt = 2
            l = i - 2
            r = i + 2
            for c in range(2):
                if word[i-1] in cycle[c]:
                    while cnt < c + 3:
                        if l < 0 or word[l] != word[i-1]:
                            break
                        cnt += 1
                        l -= 1
                    while cnt < c + 3:
                        if r >= len(word):
                            break
                        cnt += 1
                        r += 1
                        
            dels.append(word[:l+2] + word[r:])

        else:
            dels.append(word[:i] + word[i+1:])
    return dels


def _makeFile(inputfile, outputfile):
    # 파일 있는 경우는 스킵, 없는 경우만 새로 만듦
    if outputfile not in os.listdir('./'):
        wf = open(outputfile, 'wt', encoding='utf-8')
        with open(inputfile, 'rt', encoding='utf-8') as rf:
            for word in rf:
                line = []
                line.append(word[:-1]) # 개행 제거
                for d in deletes(word[:-1]):
                    line.append(d)
                wf.write('&'.join(line) + '\n')
        wf.close()


def createDeleteDict(inputFile, outputFile):  # gets input for original dict and make delete dictionary
    tempFileName = "dict_cji.txt"
    print("converting dictionary file into cji sequence")
    # 파일 있는 경우는 스킵, 없는 경우만 새로 만듦
    if tempFileName not in os.listdir('./'):
        cji_convert._makeFile(inputFile, tempFileName)
        _makeFile(tempFileName, outputFile)
    print("delete dictionary successfully created")


if __name__ == '__main__':
    createDeleteDict("dict.txt", "dict_del.txt")

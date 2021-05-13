import cheonjiin_convert as cji_convert


def deletes(word):
    deletes = [word[:i]+word[i+1:] for i in range(len(word))]
    return deletes


def _makeFile(inputfile, outputfile):
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
    cji_convert._makeFile(inputFile, tempFileName)
    _makeFile(tempFileName, outputFile)
    print("delete dictionary successfully created")


if __name__ == '__main__':
    createDeleteDict("dict.txt", "dict_del.txt")

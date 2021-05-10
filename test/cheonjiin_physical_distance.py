conv_dict = {'ㅣ': 0, 'ㆍ': 1, 'ㅡ': 2, 'ㄱ': 3, 'ㄴ': 4, 'ㄷ': 5, 'ㅂ': 6, 'ㅅ': 7, 'ㅈ': 8, 'ㅇ': 9, '#': 10}

def getConvertTable():
    f = open('./cheonjiin_physical_distance_table.txt', 'rt')
    conv_table = [list(map(int, f.readline().split())) for i in range(len(conv_dict))]
    f.close()
    return conv_table




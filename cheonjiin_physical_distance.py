import sys

avg_dist = float(1.65)
convert_dict = {
    'ㅣ': 0, 'ᆞ': 1, 'ㅡ': 2,
    'ㄱ': 3, 'ㄴ': 4, 'ㄷ': 5,
    'ㅂ': 6, 'ㅅ': 7, 'ㅈ': 8,
    'ㅇ': 9, '#': 10
    }
distance_table = list()
with open('./cheonjiin_physical_distance_table.txt', 'r') as f:
    distance_table = [list(map(float, f.readline().split())) for i in range(len(convert_dict))]


def getPhysicalDist(origin, typo):
    if len(origin) != 1 or len(typo) != 1:
        return int(-1)
    else:
        return distance_table[convert_dict[origin]][convert_dict[typo]]


def getAvgPhysicalDist():
    return avg_dist


# Damerau-Levenshtein distance based function: adjusted to calculate physical distance
def getPhysEditDist(str1, str2):
    """
    row, col = len(str_typo) + 1, len(str_origin) + 1
    table = [[float(0) for i in range(col)] for j in range(row)]

    # 초기값: 물리적 거리 평균을 초기값으로 사용 (변경 가능)
    # 원래 편집 거리 알고리즘에서는 모든 거리가 1이지만,
    # 친지인에서는 물리적 거리를 고려하므로 distance_table의 값을 사용
    table[0][1], table[1][0] = getAvgPhysicalDist(), getAvgPhysicalDist()
    for i in range(2, len(str_origin) + 1):
        table[0][i] = table[0][i - 1] + getPhysicalDist(str_origin[i - 2], str_origin[i - 1])
    for i in range(2, len(str_typo) + 1):
        table[i][0] = table[i - 1][0] + getPhysicalDist(str_typo[i - 2], str_typo[i - 1])

    # test
    print()
    for lst in table:
        for i in lst:
            print('%.2f' % i, end = '\t')
        print()
    
    for i in range(1, row):
        for j in range(1, col):
            temp1 = table[i][j - 1] + (table[0][j] - table[0][j - 1])
            temp2 = table[i - 1][j] + (table[i][0] - table[i - 1][0])
            temp3 = table[i - 1][j - 1]
            if str_typo[i - 1] != str_origin[j - 1]:
                temp3 += int(1) # 물리적 거리 평균값으로 해야 하나?
            temp4 = sys.maxsize
            if i > 1 and j > 1:
                temp4 = table[i - 2][j - 2] + int(1)    # 이 부분도 평균값으로 바꿔야 하나?
            
            table[i][j] = min(temp1, temp2, temp3, temp4)

    # test
    print()
    for lst in table:
        for i in lst:
            print('%.2f' % i, end = '\t')
        print()

    return table[row - 1][col - 1]
    """
    table = dict()
    len_str1, len_str2 = len(str1), len(str2)
    table[(-1, -1)] = 0
    table[(-1, 0)], table[0, -1] = getPhysicalDist(str1[0], str2[0]), getPhysicalDist(str1[0], str2[0])
    for i in range(0, len_str1):   # len_str1 + 1):
        table[(i, -1)] = table[(i - 1, -1)] + getPhysicalDist(str1[i], str1[i - 1]) # i + 1
    for j in range(0, len_str2):   # len_str2 + 1):
        table[(-1, j)] = table[(-1, j - 1)] + getPhysicalDist(str2[j], str2[j - 1]) # j + 1

    for i in range(len_str1):
        for j in range(len_str2):
            if str1[i] == str2[j]:
                cost = float(0) # getPhysicalDist(str1[i], str2[j])
            else:
                cost = getPhysicalDist(str1[i], str2[j]) # float(1) # getAvgPhysicalDist()
            table[(i, j)] = min(
                           table[(i - 1, j)] + (table[(i, -1)] - table[(i - 1, -1)]), # 1, # deletion
                           table[(i, j - 1)] + (table[(-1, j)] - table[(-1, j - 1)]), # 1, # insertion
                           table[(i - 1, j - 1)] + cost # substitution
                          )

            if i and j and str1[i] == str2[j - 1] and str1[i - 1] == str2[j]:
                table[(i, j)] = min(table[(i, j)], table[i - 2,j - 2] + cost) # transposition

    return table[len_str1 - 1,len_str2 - 1]


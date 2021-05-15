import sys

avg_dist = float(1.65)
convert_dict = {
    'ㅣ': 0, 'ᆞ': 1, 'ㅡ': 2,
    'ㄱ': 3, 'ㄴ': 4, 'ㄷ': 5,
    'ㅂ': 6, 'ㅅ': 7, 'ㅈ': 8,
    'ㅇ': 9, '#': 10
    }
distance_table = list()
with open('measurer/cji_physical_distance_table.txt', 'r') as f:
    distance_table = [list(map(float, f.readline().split())) for i in range(len(convert_dict))]


def get_physical_dist(origin, typo):
    if len(origin) != 1 or len(typo) != 1:
        return int(-1)
    else:
        return distance_table[convert_dict[origin]][convert_dict[typo]]


def get_avg_physical_dist():
    return avg_dist


# Damerau-Levenshtein distance based function: adjusted to calculate physical distance
def calc_edit_dist(str_origin, str_typo):
    row, col = len(str_typo) + 1, len(str_origin) + 1
    table = [[float(0) for i in range(col)] for j in range(row)]

    # 초기값: 물리적 거리 평균을 초기값으로 사용 (변경 가능)
    # 원래 편집 거리 알고리즘에서는 모든 거리가 1이지만,
    # 친지인에서는 물리적 거리를 고려하므로 distance_table의 값을 사용
    table[0][1], table[1][0] = get_avg_physical_dist(), get_avg_physical_dist()
    for i in range(2, len(str_origin) + 1):
        table[0][i] = table[0][i - 1] + get_physical_dist(str_origin[i - 2], str_origin[i - 1])
    for i in range(2, len(str_typo) + 1):
        table[i][0] = table[i - 1][0] + get_physical_dist(str_typo[i - 2], str_typo[i - 1])
    
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
        
    return table[row - 1][col - 1]

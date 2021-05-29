import sys


NON_CJI = int(11)       # index value of non-cheonjiin input
AVERAGE_DISTANCE = float(1.61)  # average distance of all possible distance
convert_dict = {
    'ㅣ': 0, 'ᆞ': 1, 'ㅡ': 2,
    'ㄱ': 3, 'ㄴ': 4, 'ㄷ': 5,
    'ㅂ': 6, 'ㅅ': 7, 'ㅈ': 8,
    'ㅇ': 9, '#': 10, 'ELSE': 11
    }
distance_table = list()
with open('measurer/cji_physical_distance_table.txt', 'r') as f:
    for i in range(len(convert_dict)):
        distance_table.append(list(map(float, f.readline().split())))


def get_conv_dict(alphabet):
    if alphabet in convert_dict:
        return convert_dict[alphabet]
    else:
        return convert_dict['ELSE']


def get_phys_dist(origin, typo):
    if len(origin) != 1 or len(typo) != 1:
        return int(-1)
    elif origin == NON_CJI or typo == NON_CJI:
        return int(1)
    else:
        ind_origin = get_conv_dict(origin)
        ind_typo = get_conv_dict(typo)
        return distance_table[ind_origin][ind_typo]


def get_avg_dist():
    return AVERAGE_DISTANCE


# Damerau-Levenshtein distance based function: adjusted to calculate physical distance
def calc_edit_dist(str_origin, str_typo):
    row = len(str_typo) + 1
    col = len(str_origin) + 1
    table = [[float(0) for i in range(col)] for j in range(row)]

    # initial data: average physical distance (cf. Documentation)
    # in original algorithm, all distance is 1,
    # but in chinjiin, it considers physical distance.
    # So, getting distance values refer to distance table.
    table[0][1] = get_avg_dist()
    table[1][0] = get_avg_dist()
    for i in range(2, len(str_origin) + 1):
        table[0][i] = (table[0][i - 1]
                       + get_phys_dist(str_origin[i - 2], str_origin[i - 1]))
    for i in range(2, len(str_typo) + 1):
        table[i][0] = (table[i - 1][0]
                       + get_phys_dist(str_typo[i - 2], str_typo[i - 1]))
    
    for i in range(1, row):
        for j in range(1, col):
            temp1 = (table[i][j - 1]
                     # getting distance between adjacent two alphabet
                     + (table[0][j] - table[0][j - 1]))
            temp2 = (table[i - 1][j]
                     # same with above comment
                     + (table[i][0] - table[i - 1][0]))
            temp3 = table[i - 1][j - 1]
            temp4 = sys.maxsize
            if str_typo[i - 1] != str_origin[j - 1]:
                temp3 += int(1)
            if i > 1 and j > 1:
                temp4 = table[i - 2][j - 2] + int(1)
            
            table[i][j] = min(temp1, temp2,
                              temp3, temp4)
        
    return table[row - 1][col - 1]

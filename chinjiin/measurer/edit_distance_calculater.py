import sys

INF = float(sys.maxsize)
NON_CJI = int(11)  # index value of non-cheonjiin input
AVERAGE_DISTANCE = float(1.61)  # average distance of all possible distance
convert_dict = {
    'ㅣ': 0, 'ᆞ': 1, 'ㅡ': 2,
    'ㄱ': 3, 'ㄴ': 4, 'ㄷ': 5,
    'ㅂ': 6, 'ㅅ': 7, 'ㅈ': 8,
    'ㅇ': 9, '#': 10, 'ELSE': 11
}
distance_table = list()
with open('measurer/cji_physical_distance_table.txt', 'r') as f:
    for cnt in range(len(convert_dict)):
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


def get_str_phys_dist(args):
    total_len = float(0)
    for i in range(1, len(args)):
        total_len += get_phys_dist(args[i], args[i - 1])
    return total_len


# Damerau-Levenshtein distance based function: adjusted to calculate physical distance
def calc_edit_dist(str_ori, str_typ):
    # "Infinity" -- greater than maximum possible edit distance
    # Used to prevent transpositions for first characters

    # print(str_ori, str_typ)
    
    # table: (M + 2) x (N + 2) sized matrix
    table = [[INF for _ in range(len(str_typ) + 2)] for __ in range(len(str_ori) + 2)]
    table[1][1] = 0
    table[2][1] = get_avg_dist()
    table[1][2] = get_avg_dist()
    for i in range(3, len(str_ori) + 2):
        table[i][1] = table[i - 1][1] + get_phys_dist(str_ori[i - 2], str_ori[i - 3])
    for i in range(3, len(str_typ) + 2):
        table[1][i] = table[1][i - 1] + get_phys_dist(str_typ[i - 2], str_typ[i - 3])

    # Holds last row each element was encountered: DA in the Wikipedia pseudocode
    last_row = {}

    # Fill in costs
    for i in range(1, len(str_ori) + 1):
        # Current character in a
        ch_str_ori = str_ori[i - 1]

        # Column of last match on this row: DB in pseudocode
        last_match_col = 0

        for j in range(1, len(str_typ) + 1):
            # Current character in b
            ch_str_typ = str_typ[j - 1]

            # Last row with matching character
            last_match_row = last_row.get(ch_str_typ, 0)

            # Cost of substitution
            cost = float(0) if ch_str_ori == ch_str_typ else float(1)  # else some_value (치환에 대한 가중치)

            # Compute substring distance
            val_sub = table[i][j] + cost  # Substitution
            val_add = table[i + 1][j] + (table[1][j + 1] - table[1][j])  # Addition
            val_del = table[i][j + 1] + (table[i + 1][1] - table[i][1])  # Deletion
            val_trs = (table[last_match_row][last_match_col]  # Transposition
                       + max((i - last_match_row - 1), (j - last_match_col - 1))
                       + float(1))
            table[i + 1][j + 1] = min(val_sub, val_add,
                                      val_del, val_trs)

            # If there was a match, update last_match_col
            if cost == 0:
                last_match_col = j

        # Update last row for current character
        last_row[ch_str_ori] = i

    # Return last element
    return table[-1][-1]

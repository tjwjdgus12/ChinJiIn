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
dist_table_path = 'cji_physical_distance_table.txt'
if __name__ != '__main__':
    dist_table_path = 'measurer/' + dist_table_path
with open(dist_table_path, 'r') as f:
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
    else:
        ind_origin = get_conv_dict(origin)
        ind_typo = get_conv_dict(typo)
        return distance_table[ind_origin][ind_typo]


# Damerau-Levenshtein distance based function: adjusted to calculate physical distance
# first param: right keyword (something in dictionary)
# second param: keyword to fix (is input)
def calc_edit_dist(str_dict, str_input):
    # "Infinity" -- greater than maximum possible edit distance
    # Used to prevent transpositions for first characters
    
    # table: (M + 2) x (N + 2) sized matrix
    table = [[INF for _ in range(len(str_input) + 2)] for __ in range(len(str_dict) + 2)]
    table[1][1] = 0
    table[2][1] = AVERAGE_DISTANCE
    table[1][2] = AVERAGE_DISTANCE
    for i in range(3, len(str_dict) + 2):
        table[i][1] = table[i - 1][1] + get_phys_dist(str_dict[i - 2], str_dict[i - 3])
    for i in range(3, len(str_input) + 2):
        table[1][i] = table[1][i - 1] + get_phys_dist(str_input[i - 2], str_input[i - 3])

    # Holds last row each element was encountered: DA in the Wikipedia pseudocode
    last_row = {}

    # Fill in costs
    for i in range(1, len(str_dict) + 1):
        # Current character in a
        ch_str_dict = str_dict[i - 1]

        # Column of last match on this row: DB in pseudocode
        last_match_col = 0

        for j in range(1, len(str_input) + 1):
            # Current character in b
            ch_str_input = str_input[j - 1]

            # Last row with matching character
            last_match_row = last_row.get(ch_str_input, 0)

            # Cost of substitution
            cost = float(0)
            if ch_str_dict != ch_str_input:
                cost = get_phys_dist(ch_str_dict, ch_str_input)

            # Compute substring distance
            val_sub = table[i][j] + cost    # Substitution
            val_add = (table[i + 1][j]      # Addition
                       + (table[1][j + 1] - table[1][j]))   # distance from previous
            val_del = (table[i][j + 1]      # Deletion
                       + float(1))          # previous: (table[i + 1][1] - table[i][1])
            val_trs = (table[last_match_row][last_match_col]  # Transposition
                       + max((i - last_match_row - 1),
                             (j - last_match_col - 1))
                       + float(1))
            table[i + 1][j + 1] = min(val_sub, val_add,
                                      val_del, val_trs)

            # If there was a match, update last_match_col
            if cost == 0:
                last_match_col = j

        # Update last row for current character
        last_row[ch_str_dict] = i

    # Return last element
    return table[-1][-1]


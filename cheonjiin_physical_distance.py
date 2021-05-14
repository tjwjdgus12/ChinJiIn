avg_dist = float(1.566)
convert_dict = {
    'ㅣ': 0, 'ㆍ': 1, 'ㅡ': 2,
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

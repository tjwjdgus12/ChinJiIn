consonant_list = ['ㄱ', 'ㅋ', 'ㄲ',
                  'ㄴ', 'ㄹ', 'ㄴ',
                  'ㄷ', 'ㅌ', 'ㄸ',
                  'ㅂ', 'ㅍ', 'ㅃ',
                  'ㅅ', 'ㅎ', 'ㅆ',
                  'ㅇ', 'ㅁ', 'ㅇ',
                  'ㅈ', 'ㅊ', 'ㅉ',
                  ]

consonant_plus_list = {'ㄱㅅ': 'ㄳ', 'ㄴㅈ': 'ㄵ', 'ㄴㅎ': 'ㄶ', 'ㄹㄱ': 'ㄺ', 'ㄹㅁ': 'ㄻ', 'ㄹㅂ': 'ㄼ', 'ㄹㅅ': 'ㄽ',
                  'ㄹㅌ': 'ㄾ', 'ㄹㅍ': 'ㄿ', 'ㄹㅎ': 'ㅀ', 'ㅂㅅ': 'ㅄ'
                  }

vowel_list = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ',
              'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ',
              'ㅣ', 'ᆞ', 'ᆢ']

basic_vowel_list = ['ᆞ', 'ㅡ', 'ㅣ']
vowel_plus_basic = [[vowel_list.index('ㅑ'), -1, 1],  # ㅏ(0)
                    [-1, -1, -1],
                    [-1, -1, vowel_list.index('ㅒ')],  # ㅑ(2)
                    [-1, -1, -1],
                    [-1, -1, vowel_list.index('ㅔ')],  # ㅓ(4)
                    [-1, -1, -1],
                    [-1, -1, vowel_list.index('ㅖ')],  # ㅕ(6)
                    [-1, -1, -1],
                    [-1, -1, vowel_list.index('ㅚ')],  # ㅗ(8)
                    [-1, -1, 10],  # ㅘ(9)
                    [-1, -1, -1],
                    [9, -1, -1],  # ㅚ(11)
                    [-1, -1, -1],
                    [17, -1, 16],  # ㅜ(13)
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, -1],
                    [-1, -1, 14],  # ㅠ(17)
                    [13, -1, 19],  # ㅡ(18)
                    [-1, -1, -1],
                    [0, -1, -1],  # ㅣ(20)
                    [22, 8, 4],  # ᆞ(21)
                    [21, 12, 6],  # ᆢ(22)
                    ]

space_list = ['#']
l1_list = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
l3_list = [' ', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ',
           'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
adjust = 0xAC00

def hangeul_convert(keyword):
    arr_list = [consonant_list, basic_vowel_list, space_list]
    temp = list()
    ch_type = -1
    ch_index = -1
    prev_type = -1
    saved_index = -1

    keyword += 'ㄲ'

    for ch in keyword:
        ch_type = -1
        for arr in arr_list:
            if ch in arr:
                ch_type = arr
                ch_index = arr.index(ch)
                break
        if ch_type == -1:
            return "invalid value(in consonant-vowel check)"

        if prev_type != ch_type:
            if prev_type == basic_vowel_list:
                temp.append([1, vowel_list[saved_index]])
            elif prev_type != -1:
                temp.append([arr_list.index(prev_type), prev_type[saved_index]])

            if ch_type == basic_vowel_list:
                saved_index = vowel_list.index(ch)
            else:
                saved_index = ch_index

        else:
            if ch_type == basic_vowel_list:
                saved_index = vowel_plus_basic[saved_index][ch_index]
            elif ch_type == consonant_list:
                if saved_index // 3 == ch_index // 3:
                    if saved_index % 3 == 2:
                        saved_index -= 2
                    else:
                        saved_index += 1

                else:
                    temp.append([arr_list.index(prev_type), prev_type[saved_index]])
                    saved_index = ch_index
            elif ch_type == space_list:
                temp.append([arr_list.index(prev_type), prev_type[saved_index]])
        prev_type = ch_type

    level = 0
    element = [0, 0, 0, 0]

    result = ''

    for i in range(len(temp)):
        if temp[i][0] == 0:  # 자음일 때
            if level == 3:
                merged = consonant_plus_list.get(temp[i - 1][1] + temp[i][1], -1)
                if merged != -1:
                    element[3] = temp[i][1]
                    level += 1
                else:
                    result += getCharUnicode(element, 3)
                    element[0] = temp[i][1]
                    element[1] = 0
                    element[2] = 0
                    level = 1
            elif level == 0:
                element[0] = temp[i][1]
                level += 1
            elif level == 2:
                if not temp[i][1] in l3_list:
                    result += getCharUnicode(element, 2)
                    level = 1
                    element[0] = temp[i][1]
                    element[1] = 0
                    element[2] = 0
                else:
                    element[level] = temp[i][1]
                    level += 1

            else:
                if level == 4:
                    element[2] = consonant_plus_list.get(element[2] + element[3])
                    result += getCharUnicode(element, 3)
                else:   # level == 1
                    result += getCharUnicode(element, 1)
                element[0] = temp[i][1]
                element[1] = 0
                element[2] = 0
                level = 1

        elif temp[i][0] == 1:  # 모음일 때
            if level == 3:
                result += getCharUnicode(element, 2)
                element[0] = element[2]
                element[1] = temp[i][1]
                element[2] = 0
            elif level == 4:
                result += getCharUnicode(element, 3)
                element[0] = element[3]
                element[1] = temp[i][1]
                element[2] = 0

            else:
                element[1] = temp[i][1]
                element[2] = 0

            level = 2

        else:   # input 이 '#' 일때
            if i == 0:
                result += ' '
            elif temp[i - 1][0] == temp[i][0]:
                result += ' '
            else:
                result += getCharUnicode(element, level)
                element = [0,0,0,0]
                level = 0

    if level == 3:
        result += getCharUnicode(element, 3)
    elif level == 2:
        result += getCharUnicode(element, 2)
    else:
        element[2] = consonant_plus_list.get(element[2] + element[3])
        result += getCharUnicode(element, 3)
    return result

def getCharUnicode(arr, level):
    element = [0, 0, 0]
    if level < 1:
        return ''

    if level > 1:
        element[0] = l1_list.index(arr[0])
        element[1] = vowel_list.index(arr[1])
        if level > 2:
            element[2] = l3_list.index(arr[2])
    else:
        return arr[0]

    return chr(((element[0] * 21) + element[1]) * 28 + element[2] + adjust)


if __name__ == '__main__':
    test_keyword = "ㅇㅣᆞㄴ#ㄴᆞᆞㅣㅇ##ㅇㅣᆞㄴ#ㄴᆞᆞㅣㅇ##ㄴㅣᆞㄴㅡㄴ##ㅈㅣㅅㅡᆞㅇㅣᆞᆞ"
    print(hangeul_convert(test_keyword))
    # make_outputFile("./korean_corpus.txt", "corpus_output.txt")

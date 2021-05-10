import re

# 유니코드 한글 시작 : 44032, 끝 : 55199
BASE_CODE, CHOSUNG, JUNGSUNG = 44032, 588, 28

# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄱㄱㄱ', 'ㄴ', 'ㄷ', 'ㄷㄷㄷ', 'ㄴㄴ', 'ㅇㅇ', 'ㅂ', 'ㅂㅂㅂ', 'ㅅ', 'ㅅㅅㅅ', 'ㅇ', 'ㅈ', 'ㅈㅈㅈ', 'ㅈㅈ', 'ㄱㄱ', 'ㄷㄷ', 'ㅂㅂ', 'ㅅㅅ']

# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ',
                 'ㅣ']

# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄱㄱㄱ', 'ㄱㅅ', 'ㄴ', 'ㄴㅈ', 'ㄴㅅㅅ', 'ㄷ', 'ㄴㄴ', 'ㄴㄴㄱ', 'ㄴㄴㅇㅇ', 'ㄴㄴㅂ', 'ㄴㄴㅅ', 'ㄴㄴㄷㄷ', 'ㄴㄴㅂㅂ', 'ㅀ', 'ㅇㅇ', 'ㅂ', 'ㅂㅅ', 'ㅅ',
                 'ㅅㅅㅅ', 'ㅇ', 'ㅈ', 'ㅈㅈ', 'ㄱㄱ', 'ㄷㄷ', 'ㅂㅂ', 'ㅅㅅ']

JUNGSUNG_CONVERT = {'ㅏ': 'ㅣᆞ', 'ㅐ': 'ㅣᆞㅣ', 'ㅑ': 'ㅣᆞᆞ', 'ㅒ': 'ㅣᆞᆞㅣ', 'ㅓ': 'ᆞㅣ', 'ㅔ': 'ᆞㅣㅣ', 'ㅕ': 'ᆞᆞㅣ', 'ㅖ': 'ᆞᆞㅣㅣ',
                    'ㅗ': 'ᆞㅡ', 'ㅘ': 'ᆞㅡㅣᆞ', 'ㅙ': 'ᆞㅡㅣᆞㅣ', 'ㅚ': 'ᆞㅡㅣ', 'ㅛ': 'ᆞᆞㅡ', 'ㅜ': 'ㅡᆞ', 'ㅝ': 'ㅡᆞᆞㅣ', 'ㅞ': 'ㅡᆞᆞㅣㅣ',
                    'ㅟ': 'ㅡᆞㅣ', 'ㅠ': 'ㅡᆞᆞ', 'ㅡ': 'ㅡ', 'ㅢ': 'ㅡㅣ', 'ㅣ': 'ㅣ'}


def cheonjiin_convert(test_keyword):
    split_keyword_list = list(test_keyword)
    prevJamo = ''
    wsFlag = False
    result = list()
    for keyword in split_keyword_list:
        # 한글 여부 check 후 분리
        if re.match('.*[ㄱ-ㅎㅏ-ㅣ가-힣]+.*', keyword) is not None:
            char_code = ord(keyword) - BASE_CODE
            if char_code < 0:
                continue
            char1 = int(char_code / CHOSUNG)
            if wsFlag:
                if prevJamo[-1] == CHOSUNG_LIST[char1][0]:
                    result.append('#')
                    wsFlag = False
                    prevJamo = ''
            result.append(CHOSUNG_LIST[char1])

            char2 = int((char_code - (CHOSUNG * char1)) / JUNGSUNG)
            result.append(JUNGSUNG_CONVERT[JUNGSUNG_LIST[char2]])

            char3 = int((char_code - (CHOSUNG * char1) - (JUNGSUNG * char2)))
            if char3 != 0:
                prevJamo = JONGSUNG_LIST[char3]
                result.append(JONGSUNG_LIST[char3])
                wsFlag = True
            else:
                continue
        else:
            result.append('#')
    # result
    return "".join(result)


def make_outputFile(inputfile, outputfile):
    wf = open(outputfile, 'wt', encoding='utf-8')
    with open(inputfile, 'rt', encoding='cp949') as rf:
        for line in rf:
            t = cheonjiin_convert(line.split(':')[0]) + '\n'
            wf.write(t)
    wf.close()

make_outputFile("dict.txt", "dict_cheonjiin.txt")


import re

# 유니코드 한글 시작 : 44032, 끝 : 55199
BASE_CODE, BASE_CHOSUNG, BASE_JUNGSUNG = 44032, 588, 28

# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄱㄱㄱ', 'ㄴ', 'ㄷ', 'ㄷㄷㄷ', 'ㄴㄴ', 'ㅇㅇ', 'ㅂ', 'ㅂㅂㅂ', 'ㅅ', 'ㅅㅅㅅ', 'ㅇ', 'ㅈ', 'ㅈㅈㅈ',
                'ㅈㅈ', 'ㄱㄱ', 'ㄷㄷ', 'ㅂㅂ', 'ㅅㅅ']

# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ',
                 'ㅣ']

# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄱㄱㄱ', 'ㄱㅅ', 'ㄴ', 'ㄴㅈ', 'ㄴㅅㅅ', 'ㄷ', 'ㄴㄴ', 'ㄴㄴㄱ', 'ㄴㄴㅇㅇ', 'ㄴㄴㅂ', 'ㄴㄴㅅ',
                 'ㄴㄴㄷㄷ', 'ㄴㄴㅂㅂ', 'ㄴㄴㅅㅅ', 'ㅇㅇ', 'ㅂ', 'ㅂㅅ', 'ㅅ', 'ㅅㅅㅅ', 'ㅇ', 'ㅈ', 'ㅈㅈ', 'ㄱㄱ', 'ㄷㄷ', 'ㅂㅂ', 'ㅅㅅ']

CHOSUNG_CONVERT = {'ㄱ': 'ㄱ', 'ㄲ': 'ㄱㄱㄱ', 'ㄴ': 'ㄴ', 'ㄷ': 'ㄷ', 'ㄸ': 'ㄷㄷㄷ', 'ㄹ': 'ㄴㄴ', 'ㅁ': 'ㅇㅇ', 'ㅂ': 'ㅂ',
                'ㅃ': 'ㅂㅂㅂ', 'ㅅ': 'ㅅ', 'ㅆ': 'ㅅㅅㅅ', 'ㅇ': 'ㅇ', 'ㅈ': 'ㅈ', 'ㅉ': 'ㅈㅈㅈ', 'ㅊ': 'ㅈㅈ', 'ㅋ': 'ㄱㄱ',
                'ㅌ': 'ㄷㄷ', 'ㅍ': 'ㅂㅂ', 'ㅎ': 'ㅅㅅ'}

JONGSUNG_CONVERT = {'ㄳ': 'ㄱㅅ', 'ㄵ': 'ㄴㅈ', 'ㄶ': 'ㄴㅅㅅ', 'ㄺ': 'ㄴㄴㄱ', 'ㄻ': 'ㄴㄴㅇㅇ',
                    'ㄼ': 'ㄴㄴㅂ', 'ㄽ': 'ㄴㄴㅅ', 'ㄾ': 'ㄴㄴㄷㄷ', 'ㄿ': 'ㄴㄴㅂㅂ', 'ㅀ': 'ㄴㄴㅅㅅ', 'ㅄ': 'ㅂㅅ'}

JUNGSUNG_CONVERT = {'ㅏ': 'ㅣᆞ', 'ㅐ': 'ㅣᆞㅣ', 'ㅑ': 'ㅣᆞᆞ', 'ㅒ': 'ㅣᆞᆞㅣ', 'ㅓ': 'ᆞㅣ', 'ㅔ': 'ᆞㅣㅣ', 'ㅕ': 'ᆞᆞㅣ', 'ㅖ': 'ᆞᆞㅣㅣ',
                    'ㅗ': 'ᆞㅡ', 'ㅘ': 'ᆞㅡㅣᆞ', 'ㅙ': 'ᆞㅡㅣᆞㅣ', 'ㅚ': 'ᆞㅡㅣ', 'ㅛ': 'ᆞᆞㅡ', 'ㅜ': 'ㅡᆞ', 'ㅝ': 'ㅡᆞᆞㅣ', 'ㅞ': 'ㅡᆞᆞㅣㅣ',
                    'ㅟ': 'ㅡᆞㅣ', 'ㅠ': 'ㅡᆞᆞ', 'ㅡ': 'ㅡ', 'ㅢ': 'ㅡㅣ', 'ㅣ': 'ㅣ'}


def cheonjiin_convert(test_keyword):
    split_keyword_list = list(test_keyword)
    prevJamo = ''
    prevKeyword = ''
    result = list()
    for keyword in split_keyword_list:
        # 한글 여부 check 후 분리
        if re.match('.*[ㄱ-ㅎㅏ-ㅣ가-힣]+.*', keyword) is not None:
            char_code = ord(keyword) - BASE_CODE
            if char_code < 0:  # 초성 + 중성의 조합이 아닌 경우 (ㄱ, ㄴ, ㄷ, ㅏ, ㅣ, ㅜ 등)
                if keyword in CHOSUNG_CONVERT:  # 단일 자음인 경우 (ㄱ, ㄴ, ㄷ..)
                    if not prevJamo and (prevKeyword != '' or prevKeyword != 'ᆞ' or prevKeyword != '#'):  # 이전 종성이 없을 경우 (ex, 아ㄴ녕) 에서 ㄴ 전에 공백 추가
                        result.append('#')
                    result.append(CHOSUNG_CONVERT[keyword])
                    prevJamo = CHOSUNG_CONVERT[keyword]
                elif keyword in JUNGSUNG_CONVERT:  # 단일 모음인 경우 (ㅏ, ㅣ, ㅜ)
                    result.append(JUNGSUNG_CONVERT[keyword])
                else:
                    print('error has been occurred during cji_convert, keyword = ' + keyword)
                    return ""
                continue

            char1 = int(char_code / BASE_CHOSUNG)  # 초성
            if prevJamo and result[-1] != '##':  # 이전 음절에 받침이 있었고 이전 음절과 한 단어인 (띄어쓰기 없을) 경우
                if prevJamo[-1] == CHOSUNG_LIST[char1][0]:
                    result.append('#')
                    prevJamo = ''
            result.append(CHOSUNG_LIST[char1])

            char2 = int((char_code - (BASE_CHOSUNG * char1)) / BASE_JUNGSUNG)  # 중성
            result.append(JUNGSUNG_CONVERT[JUNGSUNG_LIST[char2]])

            char3 = int((char_code - (BASE_CHOSUNG * char1) - (BASE_JUNGSUNG * char2)))  # 종성
            if char3 != 0:
                prevJamo = JONGSUNG_LIST[char3]
                result.append(JONGSUNG_LIST[char3])
            else:
                prevJamo = ''
                continue
            prevKeyword = result[-1]
        else:
            if keyword == ' ':  # 띄어쓰기 처리
                if result[-1] == '#':
                    result.append('#')
                else:
                    result.append('##')
            else:
                result.append(keyword)

    return "".join(result)


def _makeFile(inputfile, outputfile):
    wf = open(outputfile, 'wt', encoding='utf-8')
    with open(inputfile, 'r') as rf:
        for line in rf:
            t = cheonjiin_convert(line.split(':')[0]) + '\n'
            wf.write(t)
    wf.close()


if __name__ == '__main__':
    testStr = "아ㅉ자증나ㅉ"
    print(cheonjiin_convert(testStr))
    # _makeFile('dict.txt', 'dict_cji.txt')


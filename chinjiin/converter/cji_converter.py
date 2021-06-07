import os
import re

# 한글 유니코드 매핑을 위함 베이스 정수 변수 정의.
# 유니코드 한글 시작 : 44032, 끝 : 55199
BASE_CODE, BASE_CHOSUNG, BASE_JUNGSUNG = 44032, 588, 28

# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = [
    'ㄱ', 'ㄱㄱㄱ', 'ㄴ', 'ㄷ', 'ㄷㄷㄷ', 'ㄴㄴ', 'ㅇㅇ', 'ㅂ', 'ㅂㅂㅂ', 'ㅅ', 'ㅅㅅㅅ', 'ㅇ', 'ㅈ', 'ㅈㅈㅈ',
    'ㅈㅈ', 'ㄱㄱ', 'ㄷㄷ', 'ㅂㅂ', 'ㅅㅅ'
    ]

# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = [
    'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ'
    ]

# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [
    ' ', 'ㄱ', 'ㄱㄱㄱ', 'ㄱㅅ', 'ㄴ', 'ㄴㅈ', 'ㄴㅅㅅ', 'ㄷ', 'ㄴㄴ', 'ㄴㄴㄱ', 'ㄴㄴㅇㅇ', 'ㄴㄴㅂ', 'ㄴㄴㅅ',
    'ㄴㄴㄷㄷ', 'ㄴㄴㅂㅂ', 'ㄴㄴㅅㅅ', 'ㅇㅇ', 'ㅂ', 'ㅂㅅ', 'ㅅ', 'ㅅㅅㅅ', 'ㅇ', 'ㅈ', 'ㅈㅈ', 'ㄱㄱ', 'ㄷㄷ', 'ㅂㅂ', 'ㅅㅅ'
    ]

# 각각 초성, 중성, 종성에 대한 변환 딕셔너리.
# 입력이 들어왔을 때 각 입력에 알맞는 천지인 변환을 제공

CHOSUNG_CONVERT = {
    'ㄱ': 'ㄱ', 'ㄲ': 'ㄱㄱㄱ', 'ㄴ': 'ㄴ', 'ㄷ': 'ㄷ', 'ㄸ': 'ㄷㄷㄷ', 'ㄹ': 'ㄴㄴ', 'ㅁ': 'ㅇㅇ', 'ㅂ': 'ㅂ',
    'ㅃ': 'ㅂㅂㅂ', 'ㅅ': 'ㅅ', 'ㅆ': 'ㅅㅅㅅ', 'ㅇ': 'ㅇ', 'ㅈ': 'ㅈ', 'ㅉ': 'ㅈㅈㅈ', 'ㅊ': 'ㅈㅈ', 'ㅋ': 'ㄱㄱ',
    'ㅌ': 'ㄷㄷ', 'ㅍ': 'ㅂㅂ', 'ㅎ': 'ㅅㅅ'
    }

JUNGSUNG_CONVERT = {
    'ㅏ': 'ㅣᆞ', 'ㅐ': 'ㅣᆞㅣ', 'ㅑ': 'ㅣᆞᆞ', 'ㅒ': 'ㅣᆞᆞㅣ', 'ㅓ': 'ᆞㅣ', 'ㅔ': 'ᆞㅣㅣ', 'ㅕ': 'ᆞᆞㅣ', 'ㅖ': 'ᆞᆞㅣㅣ',
    'ㅗ': 'ᆞㅡ', 'ㅘ': 'ᆞㅡㅣᆞ', 'ㅙ': 'ᆞㅡㅣᆞㅣ', 'ㅚ': 'ᆞㅡㅣ', 'ㅛ': 'ᆞᆞㅡ', 'ㅜ': 'ㅡᆞ', 'ㅝ': 'ㅡᆞᆞㅣ', 'ㅞ': 'ㅡᆞᆞㅣㅣ',
    'ㅟ': 'ㅡᆞㅣ', 'ㅠ': 'ㅡᆞᆞ', 'ㅡ': 'ㅡ', 'ㅢ': 'ㅡㅣ', 'ㅣ': 'ㅣ'
    }

JONGSUNG_CONVERT = {
    'ㄳ': 'ㄱㅅ', 'ㄵ': 'ㄴㅈ', 'ㄶ': 'ㄴㅅㅅ', 'ㄺ': 'ㄴㄴㄱ', 'ㄻ': 'ㄴㄴㅇㅇ',
    'ㄼ': 'ㄴㄴㅂ', 'ㄽ': 'ㄴㄴㅅ', 'ㄾ': 'ㄴㄴㄷㄷ', 'ㄿ': 'ㄴㄴㅂㅂ', 'ㅀ': 'ㄴㄴㅅㅅ', 'ㅄ': 'ㅂㅅ'
    }


# 한글 입력이 test_keyword 파라미터로 들어왔을 때 천지인 변환 시퀀스를 리턴하는 함수.
# 한글 입력인지를 regex를 사용하여 우선 판별하고, 초성 + 중성의 조합이 아닌 단일 자음 혹은 단일 모음인 경우 예외처리한다.
# 한글 입력이 아닌 경우, result 배열에 그대로 더해준다. 단 공백 문자일 경우는 직전 문자에 따라 분기한다.
# res_chosung, res_jungsung, res_jongsung 변수에는 각각 초성, 중성, 종성이 들어간다.


def convert(test_keyword):
    split_keyword_list = list(test_keyword)
    previous_jamo = ''
    result = list()
    for i in range(len(split_keyword_list)):
        keyword = split_keyword_list[i]
        previous_keyword = ''
        if i > 0:
            previous_keyword = split_keyword_list[i-1]
        if re.match('.*[ㄱ-ㅎㅏ-ㅣ가-힣]+.*', keyword) is not None:
            char_code = ord(keyword) - BASE_CODE
            if char_code < 0:  # 초성 + 중성의 조합이 아닌 경우
                if keyword in CHOSUNG_CONVERT:  # 단일 자음인 경우 (ㄱ, ㄴ, ㄷ)
                    if not previous_jamo and not previous_keyword and\
                            previous_keyword not in JUNGSUNG_LIST + ['', 'ᆞ', '#']:
                        result.append('#')  # 이전 종성이 없을 경우 (ex, 아ㄴ녕) 에서 ㄴ 전에 공백 추가
                    result.append(CHOSUNG_CONVERT[keyword])
                    previous_jamo = CHOSUNG_CONVERT[keyword]
                elif keyword in JUNGSUNG_CONVERT:  # 단일 모음인 경우 (ㅏ, ㅣ, ㅜ)
                    result.append(JUNGSUNG_CONVERT[keyword])
                else:
                    print('error has been occurred during cji_convert, keyword = ' + keyword)
                    return ""
                continue

            res_chosung = int(char_code / BASE_CHOSUNG)  # 초성
            if previous_jamo and \
                    result[-1] != '##':  # 이전 음절에 받침이 있었고 이전 음절과 한 단어인 (띄어쓰기 없을) 경우 공백 문자 추가
                if previous_jamo[-1] == CHOSUNG_LIST[res_chosung][0]:
                    result.append('#')
                    previous_jamo = ''
            result.append(CHOSUNG_LIST[res_chosung])

            res_jungsung = int((char_code - (BASE_CHOSUNG * res_chosung)) / BASE_JUNGSUNG)
            result.append(JUNGSUNG_CONVERT[JUNGSUNG_LIST[res_jungsung]])

            res_jongsung = int((char_code - (BASE_CHOSUNG * res_chosung) - (BASE_JUNGSUNG * res_jungsung)))
            if res_jongsung != 0:
                previous_jamo = JONGSUNG_LIST[res_jongsung]
                result.append(JONGSUNG_LIST[res_jongsung])
            else:
                previous_jamo = ''
                continue
        else:
            if keyword == ' ':
                if result:
                    if result[-1] == '#':
                        result.append('#')
                else:
                    result.append('##')
            else:
                if keyword == 'ᆢ':
                    result.append('ᆞ')
                    result.append('ᆞ')
                    continue
                result.append(keyword)

    return "".join(result)


# 사전 파일이 입력되었을 때, 천지인으로 변환한 사전 파일을 출력하는 함수

def make_file(dict_name):
    origin_dict_file = DICT_PATH + '%s.txt' % dict_name
    cji_dict_file = DICT_PATH + '%s_cji.txt' % dict_name   
    with open(cji_dict_file, 'wt', encoding='utf-8') as wf:
        with open(origin_dict_file, 'rt', encoding='utf-8') as rf:
            for line in rf:
                word = line.split(': ')
                new_line = convert(word[0]) + ': ' + word[1]
                wf.write(new_line)


# 사전 파일이 입력되었을 때, 천지인으로 변환한 사전 파일을 딕셔너리 형태로 리턴하는 함수

def load_cji_dict(dict_name, reset=False):
    cji_dict = dict()
    cji_dict_file = DICT_PATH + '%s_cji.txt' % dict_name
    if not os.path.isfile(cji_dict_file) or reset:
        make_file(dict_name)
    with open(cji_dict_file, 'rt', encoding='utf-8') as rf:
        for line in rf:
            word = line.split(': ')
            cji_dict[word[0]] = int(word[1])
    print('cji_converted dictionary loaded')
    return cji_dict


if __name__ == '__main__':
    DICT_PATH = 'dict/'
    testStr = "깨우ㅁᆢㄴ"
    print(convert(testStr))

else:
    DICT_PATH = 'converter/dict/'

import re, json, string

"""
초성 중성 종성 분리 하기
유니코드 한글은 0xAC00 으로부터
초성 19개, 중성21개, 종성28개로 이루어지고
이들을 조합한 11,172개의 문자를 갖는다.
한글코드의 값 = ((초성 * 21) + 중성) * 28 + 종성 + 0xAC00
(0xAC00은 'ㄱ'의 코드값)
따라서 다음과 같은 계산 식이 구해진다.
유니코드 한글 문자 코드 값이 X일 때,
초성 = ((X - 0xAC00) / 28) / 21
중성 = ((X - 0xAC00) / 28) % 21
종성 = (X - 0xAC00) % 28
이 때 초성, 중성, 종성의 값은 각 소리 글자의 코드값이 아니라
이들이 각각 몇 번째 문자인가를 나타내기 때문에 다음과 같이 다시 처리한다.
초성문자코드 = 초성 + 0x1100 //('ㄱ')
중성문자코드 = 중성 + 0x1161 // ('ㅏ')
종성문자코드 = 종성 + 0x11A8 - 1 // (종성이 없는 경우가 있으므로 1을 뺌)
"""
# 유니코드 한글 시작 : 44032, 끝 : 55199
BASE_CODE, CHOSUNG, JUNGSUNG = 44032, 588, 28

# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄱㄱㄱ', 'ㄴ', 'ㄷ', 'ㄷㄷㄷ', 'ㄴㄴ', 'ㅇㅇ', 'ㅂ', 'ㅂㅂㅂ', 'ㅅ', 'ㅅㅅㅅ', 'ㅇ',
                'ㅈ', 'ㅈㅈㅈ', 'ㅈㅈ', 'ㄱㄱ', 'ㄷㄷ', 'ㅂㅂ', 'ㅅㅅ']

# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ',
                 'ㅣ']

# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = [' ', 'ㄱ', 'ㄱㄱㄱ', 'ㄱㅅ', 'ㄴ', 'ㄴㅈ', 'ㄴㅅㅅ', 'ㄷ', 'ㄴㄴ', 'ㄴㄴㄱ', 'ㄴㄴㅇㅇ', 'ㄴㄴㅂ', 'ㄴㄴㅅ', 'ㄴㄴㄷㄷ',
                 'ㄴㄴㅂㅂ', 'ㄴㄴㅅㅅ', 'ㅇㅇ', 'ㅂ', 'ㅂㅅ', 'ㅅ', 'ㅅㅅㅅ', 'ㅇ', 'ㅈ', 'ㅈㅈ', 'ㄱㄱ', 'ㄷㄷ', 'ㅂㅂ', 'ㅅㅅ']

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
                if prevJamo:
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
                prevJamo = ''
                continue
        else:
            if keyword == ' ':
                result.append('#')
            else:
                result.append(keyword)
    return "".join(result)


def make_outputFile(inputfile, outputfile):
    wf = open(outputfile, 'wt', encoding='utf-8')
    with open(inputfile, 'rt', encoding='utf-8') as rf:
        for line in rf:
            t = cheonjiin_convert(line) + '\n'
            wf.write(t)
    wf.close()


def make_dictionary(outputFile):
    dictionary = {}
    for tag in range(1, 400):
        path = r"./NIKL Everyday Conversation corpus/SDRW200000" + format(tag, '04') + ".json"
        with open(path, 'rt', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            for utterance in json_data["document"][0]["utterance"]:
                for words in utterance["form"].split(' '):
                    word = words.strip(string.punctuation).strip(string.digits)
                    if word in dictionary:
                        dictionary[word] += 1
                    else:
                        dictionary[word] = 1

    dictionary = dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True))

    f = open(outputFile, 'wt', encoding='utf-8')
    for key, value in dictionary.items():
        f.write(cheonjiin_convert(key) + " " + str(value) + "\n")
    f.close()


if __name__ == '__main__':
    test_keyword = "안녕 안녕 나는 지수야~!"
    print(cheonjiin_convert(test_keyword))
    make_dictionary('dictionary.txt')
    # make_outputFile("./dictionary.txt", "dictionary_output.txt")


# 친지인 ( ChinJiIn, 櫬地人 )
천지인 키보드에서 오타를 줄이기 위해 고안된 프로젝트입니다. 
'천지인'에서 아래아(ㆍ)가 탈락된 오타로 이름을 지었으며, 한자는 무궁화 나무 친 ‘櫬’을 사용하여 한글 창제 원리를 기반으로 한 천지인 키보드가 한글 사용자들에게 보다 쉽게 사용될 수 있길 바라는 마음을 담았습니다. 

## 개요 Introduction

### (1)  음소 분리

친지인 프로젝트의 오타 교정 알고리즘에서 가장 중요하고 기초가 되는 부분은 음소 분리입니다. 천지인 키보드의 음소분리는 기존의 두벌식 키보드 음소분리와 차이가 큽니다.  
 ‘고양이’라는 단어로 예를 들면, 두벌식에서는 우리가 직관적으로 생각할 수 있듯이 `ㄱ, ㅗ, ㅇ, ㅑ, ㅇ, ㅇ, ㅣ`로 음소가 분리되며, 이런 방식으로 음소를 분리하는 오픈소스 프로젝트는 이미 많이 존재합니다.  
 하지만, 천지인 키보드에서는 ‘고양이’가 `ㄱ, ㆍ, ㅡ, ㅇ, ㅣ, ㆍ, ㆍ ,ㅇ , space(공백 문자), ㅇ, ㅣ`로 분리됩니다. 그렇기 때문에 두벌식 기준으로 적용된 기존의 한글 교정 알고리즘을 사용할 수 없어 천지인 자판을 기준으로 한 음소 분리부터 구현하였습니다. 

### (2)  사전 구축

친지인에서 기본으로 제공되는 사전은 3가지 데이터들로 이루어져 있습니다. 
1.   국립국어원 모두의 말뭉치 (https://corpus.korean.go.kr/main.do#down) 
국립국어원 모두의 말뭉치에서 제공하는 '일상 대화 말뭉치 2020' 버전 1.0을 사용하였습니다.
2.  @songys 님의 인공 챗봇 데이터 (https://github.com/songys/Chatbot_data) 
다음 카페 '사랑보다 아름다운 실연'에 실려 있는 이야기들에 기반한 데이터들을 사용하였습니다.
3. 국립 국어원 한국어 학습용 어휘 목록 (https://www.korean.go.kr/front/etcData/etcDataView.do?mn_id=46&etc_seq=71)

위와 같은 방법으로 구성된 것이 chinjiin/converter/dict/optimized_dict.txt 파일입니다. 
각 데이터에 존재하는 한글을 전부 단어 단위로 분절하여 빈도수를 세서 단어 사전으로 활용하였습니다. 
사전 파일에 포함된 단어의 빈도수는 이후 교정 단어 목록을 추천해 줄 때 어떤 단어를 우선적으로 보여줄지를 결정하는 역할을 합니다.

### (3)  Symspell 적용

오타 교정으로 널리 사용되는 Symspell 알고리즘을 적용하였습니다. 
Symspell의 오타 교정 알고리즘은 아래와 같습니다.
1. 단어 사전에 입력 키워드가 있는지 검사
2. 단어 사전의 delete 후보군에 입력 키워드가 있는지 검사
3. 입력 키워드의 delete 후보군이 단어사전에 있는지 검사
4. 입력 키워드의 delete 후보군이 단어사전의 delete 후보군에 있는지 검사

각각의 과정을 통해서, [Peter-Norvig Algorithm](http://norvig.com/spell-correct.html)에서 4가지 오타 유형이었던 delete, transpose, replace, insert를 모두 잡아낼 수 있습니다. 

### (4)  물리적 거리

 Symspell 알고리즘을 기반으로 하되, 키보드 자판간의 거리로 교정 단어간의 우선순위를 정했습니다. 영어 Qwerty키보드 자판의 물리적 거리를 Symspell에 적용한 [Customized-Symspell](https://github.com/MighTguY/customized-symspell)이라는 프로젝트를 찾아볼 수 있었습니다.  
 천지인 자판이 가로 3, 세로 4의 12개 배열로 이루어져 있고 실질적인 글자를 나타내는 자판은 10개라는 점에 착안해 10x10 배열에 각 자판 간의 물리적 거리를 계산하여 우선순위를 정할 때 사용하였습니다.  
거리 데이터는 chinjiin/measurer/cji_physical_distance_table.txt를,  
거리 데이터를 적용하는 코드는 chinjiin/measurer/edit_distance_calculater.py 를 참고하시면 됩니다.  
  
결과적으로 친지인은 ‘낭아지’라는 오타 단어를 입력받았을 때 ‘강아지’, ‘망아지’ 등의 교정 후보가 있는 상황에서  ‘ㄱ’ 자판이 ‘ㅁ’ 자판보다 ‘ㄴ’ 자판과 물리적으로 가깝기 때문에 ‘강아지’를 우선적으로 추천해줍니다. 

## 설치 및 환경 Installation and Environment

**3.8 버전 이상의 파이썬 (Python 3.8+)** 이 필요합니다.  **utf-8 인코딩된 한글**만 지원합니다. 

원하는 디렉터리에 clone하여 받아주세요.  
```git clone https://github.com/tjwjdgus12/ChinJiIn.git```

파이썬 환경에서 다운 받은 친지인 모듈을 import 하여 사용하실 수 있습니다.  
```import chinjiin```

## 사용법 How to Use
### 단어 교정
단순 단어 교정을 위해서는 word_fixer의 direct_fix 함수를 사용하시면 됩니다.
word_fixer의 direct_fix함수는 사전 데이터에 기반하여 가장 추천 점수가 높은 단어 하나만 return 합니다.
```
import word_fixer
print(word_fixer.direct_fix('교정할 단어'))
```

보다 상세한 결과를 원하신다면, word_fixer의 more_fix함수를 사용하시면 됩니다.
word_fixer의 more_fix 함수는 사전 데이터에 기반하여 추천할 단어 목록을 정렬하여 점수가 높은 순으로 출력해줍니다.
```
import word_fixer
word_fixer.more_fix('교정할 단어')
```
### 문장 교정
문장 교정을 위해서는 chinjiin의 fix함수를 사용하시면 됩니다.
단어 단위로 direct_fix를 불러와 교정이 이루어집니다.
```
import chinjiin
print(chinjiin.fix('교정할 문장'))
```
파일 안의 모든 한글을 교정하시려면 chinjiin의 fix_file, 폴더 안에 있는 모든 한글을 교정하시려면 chinjin의 fix_dir을 사용하시면 됩니다. 
```
import chinjiin
chinjiin.fix_file('원본 파일 이름', '출력 파일 이름')
chinjiin.fix_dir('원본 폴더 디렉터리')
```
### 사전 로딩 
다른 사전 데이터를 넣어 테스트 하시려면,  load_dict 함수로 사전을 로딩할 수 있습니다.
```
import word_fixer
load_dict('파일 이름')
```
사전은 **반드시** utf-8로 인코딩되어 있어야 하고, **"단어: 빈도수"** 의 형태로 각각 한 줄을 이루고 있어야 합니다. 
chinjiin/converter/dict 폴더의 여러 사전을 참고하시면 되겠습니다. 
delete 사전 파일은 pickle 파일로 저장됩니다. 천지인 변환 사전 파일은 txt 파일로 저장됩니다. 

## 기여 Contribution
친지인은 코드 기여 및 버그 제보를 해주시는 개발자분들을 늘 환영합니다.
### 버그 제보 Bug Report
Issues 탭에서 Create New Issue를 통해 제보해주시면 감사합니다!!
제목은 bug: 태그로 시작하면서 내용이 잘 표현 될 수 있게 작성해주시고, 어떤 모듈에서 발생하는 것인지 인지하고 계시다면 제보시 아래의 사람들을 assign 해주시면 조금 더 빠른 버그 수정이 가능합니다.
1. 한글에서 천지인 시퀀스로 변환 (cji_converter 관련) : @redjen8
2. 천지인 시퀀스에서 한글로 변환 (han_converter 관련) : @SuperChobo
3. 천지인 자판의 물리적 거리 (edit_distance_calculater 관련) : @ChangminYi
4. 한글 사전  (Dictionary/ 관련) : @kindkiz 
5. word_fixer의 단어 교정 (word_fixer 및 chinjin 관련) : @tjwjdgus12
### 코드 기여 Code Contribution
Pull Request를 열어주시면 최대한 빠른 시일 내에 review하여 답변 드리도록 하겠습니다. 
PR 작성 시 어떤 부분을 왜 이렇게 수정했는지에 대한 설명 꼭 남겨주시면 감사하겠습니다!

## 참조 References
한글 자모음 분리: @neotune 님의 https://github.com/neotune/python-korean-handler/blob/master/korean_handler.py. 

한글 사전: @songys 님의 https://github.com/songys/Chatbot_data, K-ICT의 한글형태소사전(cc by-sa 2.0 LICENSE), 국립국어원의 한국어학습용어휘목록.

SymSpell: https://github.com/wolfgarbe/SymSpell

Customized-SymSpell: https://github.com/MighTguY/customized-symspell

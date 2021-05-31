# -*- coding: utf-8 -*-
from dicts.chatbot_dictionary import chatbot_dictionary
from dicts.corpus_dictionary import corpus_dictionary
from dicts.korean_word_list_dictionay import kor_dictionary


f = open("dictionary.txt", "wt", encoding="utf-8")
chatbot_dict = chatbot_dictionary()
corpus_dict = corpus_dictionary()
kor_dict = kor_dictionary()

# it is do not working because corpus data is not uploaded
for key, value in corpus_dict.items():
    if value == 1:
        break
    f.write(key + ": " + str(value) + "\n")

for key, value in chatbot_dict.items():
    f.write(key + ": " + str(value) + "\n")

for key, value in kor_dict.items():
    f.write(key + ": " + str(value) + "\n")
f.close()


if __name__ == "__main__":
    print("통합 사전 생성")

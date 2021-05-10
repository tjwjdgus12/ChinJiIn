# -*- coding: utf-8 -*-
import json
import string
import re
# Building a dictionary of frequency words
# Reference: National Institute of the Korean Language

hangul = re.compile("[^ \u3131-\u3163\uac00-\ud7a3]+")
dictionary = {}
for tag in range(1, 2233):
    path = r"./NIKL Everyday Conversation corpus/SDRW200000" + format(tag, '04') + ".json"
    with open(path, encoding='UTF8') as json_file:
        json_data = json.load(json_file)
        for utterance in json_data["document"][0]["utterance"]:
            for words in utterance["form"].split(' '):
                word = words.strip(string.punctuation).strip(string.digits)
                word = hangul.sub("", word)
                if word == "":
                    continue
                if word in dictionary:
                    dictionary[word] += 1
                else:
                    dictionary[word] = 1


dictionary = dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True))


f = open('corpus_dictionary.txt', 'w')
for key, value in dictionary.items():
    f.write(key + ": " + str(value) + "\n")
f.close()


if __name__ == "__main__":
    print(json.dumps(dictionary, indent='\t', ensure_ascii=False))

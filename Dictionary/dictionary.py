# -*- coding: utf-8 -*-
import json
import string
# Building a dictionary of frequency words
# Reference: National Institute of the Korean Language

dictionary = {}
for tag in range(1, 400):
    path = r"./NIKL Everyday Conversation corpus/SDRW200000" + format(tag, '04') + ".json"
    with open(path, encoding='UTF8') as json_file:
        json_data = json.load(json_file)
        for utterance in json_data["document"][0]["utterance"]:
            for words in utterance["form"].split(' '):
                word = words.strip(string.punctuation).strip(string.digits)
                if word == '' or word.encode().isalpha():
                    continue
                if word in dictionary:
                    dictionary[word] += 1
                else:
                    dictionary[word] = 1


dictionary = dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True))

f = open('dictionary.txt', 'w')
for key, value in dictionary.items():
    f.write(key + ": " + str(value) + "\n")
f.close()

if __name__ == "__main__":
    print(json.dumps(dictionary, indent='\t', ensure_ascii=False))

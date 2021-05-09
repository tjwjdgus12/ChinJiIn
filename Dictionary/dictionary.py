# -*- coding: utf-8 -*-
import json
import string
# Building a dictionary of frequency words
# Reference: National Institute of the Korean Language

dictionary = {}
with open(r'./NIKL Everyday Conversation corpus/SDRW2000000001.json', encoding='UTF8') as json_file:
    json_data = json.load(json_file)
    for utterance in json_data["document"][0]["utterance"]:
        for words in utterance["form"].split(' '):
            word = words.strip(string.punctuation)
            if word in dictionary:
                dictionary[word] += 1
            else:
                dictionary[word] = 1


dictionary = dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True))
print(json.dumps(dictionary, indent='\t', ensure_ascii=False))

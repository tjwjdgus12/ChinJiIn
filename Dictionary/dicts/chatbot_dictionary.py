# -*- coding: utf-8 -*-
import csv
import json
import string
# Building a dictionary of frequency words
# Reference: https://github.com/songys/Chatbot_data

dictionary = {}


def chatbot_dictionary():
    global dictionary
    with open("dicts/ChatbotData.csv", "r", encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        for line in reader:
            for words in line[:2]:
                for word in words.split(" "):
                    word = word.strip(string.punctuation)
                    if word == "":
                        continue
                    if word in dictionary:
                        dictionary[word] += 1
                    else:
                        dictionary[word] = 1

    dictionary = dict(sorted(dictionary.items(), key=lambda x: x[1], reverse=True))
    return dictionary


if __name__ == "__main__":
    f = open('chatbot_dictionary.txt', "wt", encoding="utf-8")
    for key, value in dictionary.items():
        f.write(key + ": " + str(value) + "\n")
    f.close()
    print(json.dumps(dictionary, indent='\t', ensure_ascii=False))

# -*- coding: utf-8 -*-
from openpyxl import load_workbook
import string
import json
# Vocabulary list for learning Korean
# Reference: National Institute of the Korean Language
dictionary = {}


def kor_dictionary():
    global dictionary
    load_wb = load_workbook('dicts/VocabularyList4LearningKor.xlsx', data_only=True)
    load_ws = load_wb["Sheet1"]
    for i in load_ws['B1':'B5966']:
        for cell in i:
            word = cell.value.strip(string.digits)
            if word in dictionary:
                dictionary[word] += 1
            else:
                dictionary[word] = 1
    return dictionary


if __name__ == "__main__":
    f = open('kor_dictionary.txt', "wt", encoding="utf-8")
    for key, value in dictionary.items():
        f.write(key + ": " + str(value) + "\n")
    f.close()
    print(json.dumps(dictionary, indent='\t', ensure_ascii=False))

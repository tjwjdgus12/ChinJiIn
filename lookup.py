# -*- coding: UTF-8 -*-

from symspellpy import SymSpell, Verbosity

sym_spell = SymSpell()
sym_spell.load_dictionary("./dictionary.txt", term_index=0, count_index=1, encoding='utf-8')

input_term = "ㅇㅣㅅㅅㄴㅡㄴ"
# Print out first 5 elements to demonstrate that dictionary is
# successfully loaded
suggestions = sym_spell.lookup(input_term, Verbosity.ALL,
                               max_edit_distance=2)
# display suggestion term, term frequency, and edit distance
for suggestion in suggestions:
    print(suggestion)
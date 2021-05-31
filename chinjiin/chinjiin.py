import word_fixer

def fix(sentence):
    words = sentence.split()
    fixed = ''
    for word in words:
        fixed += word_fixer.direct_fix(word) + ' '
    return fixed.rstrip()

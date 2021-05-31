import word_fixer

def fix(sentence):
    words = sentence.split()
    fixed = ''
    for word in words:
        fixed += word_fixer.direct_fix(word) + ' '
    return fixed.rstrip()

def fix_file(input_file):
    with open(input_file, 'rt', encoding='utf-8') as rf:
        sentence = ' '.join(rf)
        
    with open('fixed_'+input_file, 'wt') as wf:
        wf.write(fix(sentence))

while True:
    print(fix(input()))

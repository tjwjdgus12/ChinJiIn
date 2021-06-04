import os
import word_fixer


def fix(sentence):
    words = sentence.split()
    fixed = ''
    for word in words:
        fixed += word_fixer.direct_fix(word) + ' '
    return fixed.rstrip()


def fix_file(input_file, output_file='output'):
    with open(input_file, 'rt', encoding='utf-8') as rf:
        sentence = ' '.join(rf)
        
    with open(output_file, 'wt') as wf:
        wf.write(fix(sentence))


def fix_dir(path_dir):
    file_list = os.listdir(path_dir)
    for file in file_list:
        fix_file(path_dir + file, path_dir + 'fixed_' + file)


if __name__ == '__main__':
    while True:
        print(fix(input()))

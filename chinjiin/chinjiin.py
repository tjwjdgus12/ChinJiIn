import re
from pathlib import Path


HANGUL_WORD_PATTERN = re.compile(r'[ㄱ-ㅎㅏ-ㅣ가-힣]+')


def fix(sentence):
    from . import word_fixer

    return HANGUL_WORD_PATTERN.sub(
        lambda match: word_fixer.direct_fix(match.group(0)),
        sentence,
    )


def fix_file(input_file, output_file=None):
    input_path = Path(input_file)
    if output_file is None:
        output_path = input_path.with_name(
            '%s.fixed%s' % (input_path.stem, input_path.suffix)
        )
    else:
        output_path = Path(output_file)

    if input_path.resolve() == output_path.resolve():
        raise ValueError('input and output paths must be different')

    sentence = input_path.read_text(encoding='utf-8')
    output_path.write_text(fix(sentence), encoding='utf-8')
    return output_path


def fix_dir(path_dir, output_dir=None, pattern='*.txt', recursive=False):
    source_dir = Path(path_dir)
    if not source_dir.is_dir():
        raise NotADirectoryError(source_dir)

    destination_dir = Path(output_dir) if output_dir else source_dir / 'fixed'
    if source_dir.resolve() == destination_dir.resolve():
        raise ValueError('output directory must be different from input directory')

    destination_dir.mkdir(parents=True, exist_ok=True)
    files = source_dir.rglob(pattern) if recursive else source_dir.glob(pattern)
    output_files = []

    for input_path in files:
        if not input_path.is_file():
            continue
        try:
            input_path.resolve().relative_to(destination_dir.resolve())
            continue
        except ValueError:
            pass

        relative_path = input_path.relative_to(source_dir)
        output_path = destination_dir / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_files.append(fix_file(input_path, output_path))

    return output_files


if __name__ == '__main__':
    while True:
        print(fix(input()))

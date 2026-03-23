import opencc
converter = opencc.OpenCC('t2s.json')


from pathlib import Path

simplified_c = converter.convert(
    Path('zh_pud-ud-test.conllu').read_text().strip())

with open('zhs_pud-ud-test.conllu', 'w') as f:
    f.write(simplified_c)
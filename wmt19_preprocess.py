import re

input_file = "newstest2019-ende-src.en.sgm"
output_file = "newstest2019.en"

with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

segments = re.findall(r"<seg id=\"\d+\">(.*?)</seg>", text)

with open(output_file, "w", encoding="utf-8") as f:
    for seg in segments:
        f.write(seg.strip() + "\n")
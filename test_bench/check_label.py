

import re
import sys


#file = sys.argv[1]
file = "/Users/brono/GitHub/katana/transcriptions/test_bench/1-scripts/ref/ref_herring09.txt"
with open(file, 'r') as f:
    content = f.readlines()

for line in content:

    if not re.search(r"^\*[A-Z]{3}:", line):
        print(line.rstrip(), " <<<No Label>>>\n")
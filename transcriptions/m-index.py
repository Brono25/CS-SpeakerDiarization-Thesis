
import sys
import re
import os


transcript_dir = "/Users/brono/GitHub/katana/transcriptions/1-speech"

file = sys.argv[1]
output_dir = "/Users/brono/GitHub/katana/transcriptions/m-index"
file_name = re.search(r".*/1-(.*)\.txt", file).group(1)
output_file = f"/Users/brono/GitHub/katana/transcriptions/m-index/m-{file_name}.txt"


with open(file, 'r') as f:
    content = f.readlines()



def cleanLine(line):
    clean_line = re.sub(r"^\*[A-Z]{3}:", "", line)
    clean_line = re.sub(r"\[- spa\]|\[- eng\]", "$", clean_line)
    clean_line = re.sub(r"[\t,'\"?,!.]", "", clean_line) #remove punctuation
    clean_line = re.sub(r"[<>()+:&-//\\]", "", clean_line) #remove punctuation
    clean_line = re.sub(r"\x15\d+_\d+\x15", "", clean_line) #remove timestamps
    clean_line = re.sub(r"=[a-z]+", "", clean_line) #remove laughs/coughs etc
    clean_line = re.sub(r"\[\]", "", clean_line)
    return clean_line

def count_words(clean_line, p_count, s_count):

    if re.search(r"\$", clean_line):
        tmp = clean_line.split(' ')
        tmp = [x for x in tmp if x != '']
        s_count += len(tmp)
    else:
        # Find all non-tagged words (prim language)
        tmp = re.sub(r'[^ ]+@s', "", clean_line).split(' ')
        tmp = [x for x in tmp if x != '']
        p_count += len(tmp)

        # Find all secondary language tags
        tmp = re.findall(r'[^ ]+@s', clean_line)
        tmp = [x for x in tmp if x != '']
        s_count += len(tmp)
    return p_count, s_count


p_count = 0
s_count = 0
tmp = []
for i, line in enumerate(content):  
    clean_line = cleanLine(line).rstrip('\n')
    p_count, s_count = count_words(clean_line, p_count, s_count)
    


k = 2
p1 = (p_count / (p_count + s_count))
p2 = (s_count / (p_count + s_count))
Ppj2 = p1**2 + p2**2

M_index = (1 - Ppj2) / ((k - 1) * Ppj2)

print(f"{file_name}:  M-index = {M_index:.2f}")
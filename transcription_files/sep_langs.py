import shutil
import os
import re

# Open the file
file_name = "filtered_sastre09_1.txt"
out_file = "sastre09_1.txt"
with open(file_name, "r") as file:
    lines = file.readlines()

# Duplicate the file with a new name 'raw_filename.txt'
raw_file_name = "backup_" + os.path.basename(file_name)
shutil.copyfile(file_name, raw_file_name)



def group_languages(words):
    groups = []
    group = ""
    for word in words:
        if re.search(r"@s", word):
            if group and "@s" not in group:
                groups.append(group.strip())
                group = ""
            group += word + " "
        else:
            if group and "@s" in group:
                groups.append(group.strip())
                group = ""
            group += word + " "
    if group:
        groups.append(group.strip())
    return groups

def split_into_lines(groups, label, timestamp):
    new_lines = []
    for group in groups:
       
        new_lines.append(f"{label} ! {group} {timestamp}\n")
    return new_lines

new_content = []
for line in lines:

    label, utterance = line.split(" ", 1)
    timestamp = re.search(r"(\d+_\d+)", line).group(1)
    utterance = re.sub(r"\d+_\d+", '', utterance).rstrip('\n ')
    words = utterance.split()
    if "@s" not in line:
        new_content.append(line)
    else:
        groups = group_languages(words)
        new_lines = split_into_lines(groups, label, timestamp)
        new_content.extend(new_lines)

for line in new_content:
    print(line, end='')

#Save the modified lines back to the original file
with open(out_file, "w") as file:
   file.writelines(new_content)

 
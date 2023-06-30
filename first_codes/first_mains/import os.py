import os
def find(name, path):
    files = []
    for i in os.listdir(path):
        if os.path.isfile(os.path.join(path,i)) and name in i:
            files.append(i)
    files = files[0]
    return files
data = find("astrochop_14", "./chop")
print(data)
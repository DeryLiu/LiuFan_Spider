import re
f = open("./error.txt", "r")
ff = open("./111.txt", "aw")
content = f.read()
# print content
list_asins = re.findall(r"'(.*?)\\n'", content)
for asin in list_asins:
    # print asin
    ff.write(asin + "\n")

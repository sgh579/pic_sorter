import re
pattern = r'![[].*?[]]\(.*?(sor.+?)\)' 
# matches = re.findall(pattern,content)
res = []
with open('W8/w8.md','r',encoding='utf-8') as fp:
    con = fp.readlines()
    for line in con:
        match = re.findall(pattern,line)
        if match != []:
            res.append(match)

# print(res)
for i in res:
    print(i)
import sys, re
p = sys.argv[1]
s = open(p, encoding='utf-8').read()
n = len(re.findall(r'[\u4e00-\u9fff]', s))
print(n)

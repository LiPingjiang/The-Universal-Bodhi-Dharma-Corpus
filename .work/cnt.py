import sys, re
for p in sys.argv[1:]:
    t = open(p, encoding='utf-8').read()
    n = len(re.findall(r'[\u4e00-\u9fff]', t))
    print(f"{n}\t{p}")

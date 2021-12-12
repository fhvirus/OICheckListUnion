import re

def getProblemStatus(text):
    pattern_solved = re.compile(r"var (\w+)_problems = \[(.*)\]", re.MULTILINE)
    match = pattern_solved.findall(text)

    mp = dict()

    for m in match:
        if m[1] == '':
            continue
        mp[m[0]] = []
        ids = m[1].split(', ')
        for i in ids:
            mp[m[0]].append(int(i))

    return mp

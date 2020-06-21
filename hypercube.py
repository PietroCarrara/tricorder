def tesse_fix(s):
    s = s.strip()
    s = fix_i(s)

    return s.strip()

def fix_i(s):
    if (s.startswith('| ')):
        s = list(s)
        s[0] = 'I'
        s = ''.join(s)

    return s.replace(' | ', ' I ')
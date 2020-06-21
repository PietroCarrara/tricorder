def tesse_fix(s):
    s = s.strip()
    s = fix_i(s)
    s = fix_apos(s)

    return s.strip()

def fix_i(s):
    if (s.startswith('| ')):
        s = list(s)
        s[0] = 'I'
        s = ''.join(s)

    return s.replace(' | ', ' I ')

def fix_apos(s):
    return s.replace('’', "'").replace('‘', "'")
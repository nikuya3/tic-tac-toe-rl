def find(s, ch):
    return [index for index, s_c in enumerate(s) if s_c == ch]


def replace(s, i, c):
    return s[:i] + c + s[i + 1:]
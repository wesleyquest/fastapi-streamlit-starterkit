
def str_to_asterisk(string):
    if len(string) <= 4:
        string = "*"*len(string)
    else:
        string = "*"*(len(string)-4) + string[-4:]

    return string



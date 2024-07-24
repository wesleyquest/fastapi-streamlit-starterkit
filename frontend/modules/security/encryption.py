
def str_to_asterisk(string):
    if len(string) <= 4:
        string = "****"
    else:
        string = "****" + string[-4:]

    return string



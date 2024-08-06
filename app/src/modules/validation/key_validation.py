import re


def validate_openai_api_key(data):
    exp = re.compile("[a-zA-Z0-9-]{4,}")

    #validation
    val = exp.match(data)
    if val:
        return True
    else:
        return False


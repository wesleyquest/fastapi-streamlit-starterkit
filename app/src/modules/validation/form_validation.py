import re


#signup form validation
def validate_email(data):
    exp = re.compile('^[a-zA-Z0-9+-\_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    
    #validation
    val = exp.match(data)

    if val:
        return True
    else:
        return False

def validate_username(data):
    exp = re.compile('.{4,}')

    #validation
    val = exp.match(data)

    if val:
        return True
    else:
        return False
    
def validate_password(data):
    exp = re.compile('.{4,}')

    #validation
    val = exp.match(data)

    if val:
        return True
    else:
        return False

def validate_password_re(data, password):

    #password correction
    if data == password:
        return True
    
    return False

def validate_text(data):
    exp = re.compile('.{10,}')

    #validation
    val = exp.match(data)

    if val:
        return True
    else:
        return False



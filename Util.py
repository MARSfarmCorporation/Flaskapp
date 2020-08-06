import string

def decode_secret(secret):
    
    result = ""

    for char in secret:
        code = ord(char)
        if code is 46:
            code += 1

        result += chr((code - 1))

    return result
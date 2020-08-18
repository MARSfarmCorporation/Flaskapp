'''
Util.py is a collection of utility functions that 
will be used repeatedlly but have no dependencies
on third-party library.

Last Modified: 8/17/20
'''
import string

'''
This function take the encoded email in the url
and decode it by pushing each character to the 
previous one in ASCII encoding, except for "."
'''
def decode_secret(secret):
    
    result = ""

    for char in secret:
        code = ord(char)
        if code is 46: #"." is an exception
            code += 1

        result += chr((code - 1))

    return result
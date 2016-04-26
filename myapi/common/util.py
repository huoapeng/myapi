import re

# @staticmethod
def valid_email(email_str):
    m = re.match(r'(\w+)@(\w+)[.](\w+)', email_str)
    if m is None:
        return False
    else:
        return True

def md5(str):
    import hashlib
    import types
    if type(str) is types.StringType:
        m = hashlib.md5()   
        m.update(str)
        return m.hexdigest()
    else:
        return ''
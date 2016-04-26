import re

# @staticmethod
def valid_email(email_str):
    m = re.match(r'(\w+)@(\w+)[.](\w+)', email_str)
    if m is None:
        return False
    else:
        return True
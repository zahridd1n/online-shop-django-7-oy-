import random
import string


def code_generate():
    code = "".join(random.sample(string.ascii_letters, 14))
    return code

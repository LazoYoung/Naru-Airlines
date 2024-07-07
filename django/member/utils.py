import random
import string


def get_random_string(length, lowercase=False):
    seq = string.ascii_lowercase + string.digits if lowercase else string.ascii_letters + string.digits
    return ''.join(random.choice(seq) for _ in range(length))


def get_random_password(length=8):
    pw = get_random_string(length - 1) + str(random.randint(0, 9))
    return pw


def get_random_email():
    return get_random_string(12, lowercase=True) + "@mailtest.org"

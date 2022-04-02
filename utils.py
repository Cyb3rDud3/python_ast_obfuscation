from random import randint

def random_string(minlength, maxlength):
    return ''.join(chr(randint(0x61, 0x7a))
                   for x in range(randint(minlength * 2, maxlength *2)))


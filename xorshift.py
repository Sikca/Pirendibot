import random

def xorshift32(x):
    x ^= x << 13
    x ^= x >> 17
    x ^= x << 5
    return x

print(xorshift32(random.randint(1,100)))
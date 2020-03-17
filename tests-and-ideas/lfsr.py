import inspect
import random
from collections import defaultdict
from pprint import pprint

coefs = {
    3:  [3, 2],
    4:  [4, 3],
    5:  [5, 3],
    6:  [6, 5],
    7:  [7, 6],
    8:  [8, 6, 5, 4],
    9:  [9, 5],
    10: [10, 7],
    11: [11, 9],
    12: [12, 6, 4, 1],
    13: [13, 4, 3, 1],
    14: [14, 5, 3, 1],
    15: [15, 14],
    16: [16, 15, 13, 4],
    17: [17, 14],
    18: [18, 11],
    19: [19, 6, 2, 1],
    20: [20, 17],
    21: [21, 19],
    22: [22, 21],
    23: [23, 18],
    24: [24, 23, 22, 17],
    25: [25, 22],
    26: [26, 6, 2, 1],
    27: [27, 5, 2, 1],
    28: [28, 25],
    29: [29, 27],
    30: [30, 6, 4, 1],
    31: [31, 28],
    32: [32, 22, 2, 1],
}
def xnor(samples):
    ret = samples[0]
    for sample in samples[1:]:
        ret = not(sample ^ ret)
    return ret

vec_to_int = lambda vec: sum([int(v)*e
                              for v,e in zip(vec,
                                             [2**i for i in range(len(vec))])])

def lfsr(nb_bits=4):
    assert nb_bits >= 3
    assert nb_bits <= 32
    seed_gen = lambda : [random.choice([True, False]) for _ in range(nb_bits)]
    register = seed_gen()
    print(f"{register=}")
    while True:
        new_bit = xnor(samples=[register[c-1] for c in coefs[nb_bits]])
        register = [new_bit] + register[:-1]
        yield register

bins=defaultdict(int)
for i, r in enumerate(lfsr(nb_bits=5)):
    pprint(r)
    bins[vec_to_int(r)] += 1
    if i > 1024:
        break
pprint(bins)

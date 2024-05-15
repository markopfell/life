import numpy as np
from pylfsr import LFSR


# h(x) = x8 + x6 + x4 + x3 + x2 + x + 1
# [1, 0, 1, 0, 1, 1, 1, 1]
state = [1, 1, 1, 1, 1, 1, 1, 1]
# fpoly = [1, 2, 3, 4, 6, 8]
fpoly = [8, 6, 4, 3, 2, 1]
# fpoly = [8, 7, 5, 3]

L = LFSR(fpoly=fpoly,initstate=state, verbose=True, conf='fibonacci')

# # K cycles
k=len(state)*256
seq  = L.runKCycle(k)
#Cycles of a full period, #cycles = expected period of LFSR
# L.runFullCycle()  # Depreciated
seq = L.runFullPeriod()

full_sequence = list(L.arr2str(seq))
full_sequence = list(map(int, list(reversed(full_sequence))))
print(full_sequence)
# print(L.arr2str(seq))
# print('')

# L.info()
#
# L.Viz()




golden = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0]
# golden = [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0]
print(golden)

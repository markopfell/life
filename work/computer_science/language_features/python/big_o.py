import numpy
import time

# Create array of 8000 random integers from 0 to 7
array = numpy.random.randint(0, 8, size=8000)

print(array)
print(f"Shape: {array.shape}")
print(f"Min value: {array.min()}, Max value: {array.max()}")

start_perf = time.perf_counter()

for index, value in enumerate(array):
    pass
    # print(f"Index {index}: {value}") 

end_perf = time.perf_counter()
elapsed_perf = end_perf - start_perf
print(f"Elapsed time (perf_counter): {elapsed_perf:.6f} seconds")
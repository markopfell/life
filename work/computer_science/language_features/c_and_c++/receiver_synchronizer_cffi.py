from cffi import FFI
import numpy as np
import time

# Create FFI instance
ffi = FFI()

# Define the C function signature
ffi.cdef("""
    double loop_through_array(uint8_t* array, int size);
""")

# Define the C source code
c_source = """
#include <stdint.h>
#include <time.h>

double loop_through_array(uint8_t* array, int size) {
    clock_t start = clock();
    
    for (int i = 0; i < size; i++) {
        uint8_t value = array[i];
        // Do nothing
    }
    
    clock_t end = clock();
    return (double)(end - start) / CLOCKS_PER_SEC;
}
"""

# Compile the C code
ffibuilder = ffi.verify(c_source)

# Create array of 8000 random integers from 0 to 7
array = np.random.randint(0, 8, size=8000, dtype=np.uint8)

print(f"Array created with shape: {array.shape}")
print(f"Min value: {array.min()}, Max value: {array.max()}")

# Convert NumPy array to C pointer
array_ptr = ffi.cast("uint8_t*", array.ctypes.data)

# Call the C function
start_py = time.perf_counter()
elapsed_c = ffibuilder.loop_through_array(array_ptr, len(array))
end_py = time.perf_counter()

print(f"\nElapsed time (C internal): {elapsed_c*1E6:.3f} microseconds")
print(f"Elapsed time (Python wrapper): {(end_py - start_py)*1E6:.3f} microseconds")

# For comparison, run Python loop
start_python = time.perf_counter()
for index, value in enumerate(array):
    pass
end_python = time.perf_counter()

print(f"Elapsed time (Pure Python): {(end_python - start_python)*1E6:.3f} microseconds")
print(f"\nSpeedup: {(end_python - start_python) / elapsed_c:.1f}x")
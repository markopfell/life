import numpy

<<<<<<< HEAD
BYTE_TO_BITS = 8
UINT16_BYTES = 2

packet_payload_bytes = bytearray([0x00]*30840)

bit_length = len(packet_payload_bytes)*BYTE_TO_BITS
bit_length_bits_str = bin(bit_length)[2:].zfill(UINT16_BYTES*BYTE_TO_BITS)
bit_length_bits_str_array = list(bit_length_bits_str)
bit_length_bits = numpy.array(bit_length_bits_str_array, dtype=numpy.uint8)
bit_length_bits = numpy.array(bit_length_bits, dtype=numpy.bool)

print(bit_length_bits_str, len(bit_length_bits_str))
print(bit_length_bits_str_array, len(bit_length_bits_str_array))
print(bit_length_bits, len(bit_length_bits))
print(bit_length_bits[0:4], len(bit_length_bits[0:4]))
#111100001111000000 18
#['1', '1', '1', '1', '0', '0', '0', '0', '1', '1', '1', '1', '0', '0', '0', '0', '0', '0'] 18
#[ True  True  True  True False False False False  True  True  True  True False False False False False False] 18
#[ True  True  True  True] 4
=======
def binary_array_to_int(arr):
    # Convert to integer using powers of 2
    powers = 2 ** numpy.arange(len(arr))[::-1]
    decimal = numpy.sum(arr * powers)
    return int(decimal)

def binary_array_to_float(arr):
    # Convert to float using powers of 2
    powers = 2 ** numpy.arange(len(arr))[::-1]
    decimal = numpy.sum(arr * powers)
    return decimal

_32_bit_synchronization_pattern_bits = [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
_32_bit_synchronization_pattern_value= binary_array_to_float(_32_bit_synchronization_pattern_bits)
_32_bit_synchronization_pattern_bytes = numpy.array([_32_bit_synchronization_pattern_value], dtype=numpy.uint32).view(numpy.uint8)[:4]

print(_32_bit_synchronization_pattern_bytes, type(_32_bit_synchronization_pattern_bytes[0]))
>>>>>>> da65086 (testing float which is 32 bits greater than 16 bit int conversion to binary)

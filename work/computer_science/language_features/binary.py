import numpy

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
#%%
import rawpy
import imageio
import numpy as np
from heapq import heappush, heappop, heapify
from collections import defaultdict

# %%
image_name = "reh"
image_type = ".ARW"
# %%
example_array = np.array([[[1, 2, 3, 4, 5],
                          [6, 7, 8, 9, 10],
                          [11, 12, 13, 14, 15],
                          [16, 17, 18, 19, 20]],
                        
                         [[21, 22, 23, 24, 25],
                          [26, 27, 28, 29, 30],
                          [31, 32, 33, 34, 35],
                          [36, 37, 38, 39, 40]],
                        
                         [[41, 42, 43, 44, 45],
                          [46, 47, 48, 49, 50],
                          [51, 52, 53, 54, 55],
                          [56, 57, 58, 59, 60]]])

print(example_array.shape)
print(example_array.flatten())

# %%
output_type = ".png"
base_input_path = '../../images/input/'
base_output_path = '../../images/output/'

image_path = base_input_path + image_name + image_type
output_path = base_output_path + image_name + output_type

# %%
# Read CR2 file using rawpy
with rawpy.imread(image_path) as raw:
    # Perform demosaicing to obtain RGB image
    rgb_image = raw.postprocess()

# %%
image_array = np.array(rgb_image)
# Convert raw data to a NumPy array
print(image_array.shape)

# %%
# work with np array
flat_arr = image_array.flatten()
print("Size of img: " + str(len(flat_arr)) + " Byte") # 72721728 Byte

# %%
print(flat_arr.min())
print(flat_arr.max())
print(flat_arr[0:10])

# %%
def huffman_tree(freq):
    heap = [[weight, [symbol, ""]] for symbol, weight in freq.items()]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return heap[0][1:]

def huffman_compress(data):
    freq = defaultdict(int)
    for symbol in data:
        freq[symbol] += 1
    codes = huffman_tree(freq)
    codes_dict = dict(codes)
    transformed = [codes_dict.get(symbol) for symbol in data]
    compressed_data = ''.join(transformed)
    return compressed_data, codes_dict

def huffman_decompress(compressed_data, codes):
    reversed_codes = {code: symbol for symbol, code in codes.items()}
    current_code = ""
    decompressed_data = []
    for bit in compressed_data:
        current_code += bit
        if current_code in reversed_codes:
            decompressed_data.append(reversed_codes[current_code])
            current_code = ""
    return decompressed_data

# %%


example_arr = flat_arr
print(example_arr.shape)

# Huffman-Kompression
compressed_data, codes = huffman_compress(example_arr)

print("Size of original data: " + str(len(example_arr) * 8) + " Bits")

print("Size of Huffman compressed data: " + str(len(compressed_data)) + " Bit")

# size of dict: key: 1 Byte, Value 2 Byte, worst case Annahme
print("Size of dict: " + str(len(codes) * 3 * 8) + " Bits")

# Huffman-Dekompression
decompressed_array = huffman_decompress(compressed_data, codes)
print("Size of Huffman decompressed data: " + str(len(decompressed_array) * 8) + " Bits")

# %%

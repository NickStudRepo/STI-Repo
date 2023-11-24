import numpy as np
from heapq import heappush, heappop, heapify
from collections import defaultdict

# import local file
import sys
sys.path.append('./')
from ImageConversion.imageToNpArr import get_flat_np_arr_from_image
from ImageConversion.imageToNpArr import read_png_to_array
from Helper.run_and_time_func import run_and_time_function_1_2
from Helper.run_and_time_func import run_and_time_function_2_1


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

def huffman_all_get_compressed(input):
    # Huffman-Kompression
    # compressed_data, codes = huffman_compress(flat_np_arr)
    compressed_data, codes = run_and_time_function_1_2(huffman_compress, input, "Huffman Compression")

    # Huffman-Dekompression
    # decompressed_array = huffman_decompress(compressed_data, codes)
    decompressed_array = run_and_time_function_2_1(huffman_decompress, compressed_data, codes, "Huffman Decompression")

    # Sizes: 
    print("Size of original data: " + str(len(input)) + " Byte")

    print("Size of Huffman compressed data: " + str(len(compressed_data)/8) + " Byte")    
    # size of dict: key: 1 Byte, Value 2 Byte, worst case 
    print("Size of dict: " + str(len(codes) * 3) + " Byte")

    print("Size of Huffman decompressed data: " + str(len(decompressed_array)) + " Byte")

    return compressed_data, codes



if __name__ == "__main__":

    # flat_np_arr = get_flat_np_arr_from_image("reh", "ARW")
    flat_np_arr = read_png_to_array("folie.png")

    # Huffman-Kompression
    # compressed_data, codes = huffman_compress(flat_np_arr)
    compressed_data, codes = run_and_time_function_1_2(huffman_compress, flat_np_arr, "Huffman Compression")

    # Huffman-Dekompression
    # decompressed_array = huffman_decompress(compressed_data, codes)
    decompressed_array = run_and_time_function_2_1(huffman_decompress, compressed_data, codes, "Huffman Decompression")

    # Sizes: 
    print("Size of original data: " + str(len(flat_np_arr)) + " Byte")

    print("Size of Huffman compressed data: " + str(len(compressed_data)/8) + " Byte")    
    # size of dict: key: 1 Byte, Value 2 Byte, worst case 
    print("Size of dict: " + str(len(codes) * 3) + " Byte")

    print("Size of Huffman decompressed data: " + str(len(decompressed_array)) + " Byte")
    


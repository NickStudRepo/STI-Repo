# np arr to text file
import numpy as np
import sys

sys.path.append('./')
from Huffman.huffman import huffman_compress
from Huffman.huffman import huffman_decompress

if __name__ == "__main__":

    # load LZ77 compressed file 
    file_path = "./files/LZ77/compressedImage.txt"
    flat_np_arr = np.fromfile(file_path, dtype=np.uint8)

    # Huffman-Kompression
    compressed_data, codes = huffman_compress(flat_np_arr)

    print("Size of original data: " + str(len(flat_np_arr) * 8) + " Bits")
    print("Size of Huffman compressed data: " + str(len(compressed_data)) + " Bits")

    # size of dict: key: 1 Byte, Value 2 Byte, worst case Annahme
    print("Size of dict: " + str(len(codes) * 3 * 8) + " Bits")

    # Huffman-Dekompression
    decompressed_array = huffman_decompress(compressed_data, codes)
    print("Size of Huffman decompressed data: " + str(len(decompressed_array) * 8) + " Bits")
# np arr to text file
import numpy as np
import sys

sys.path.append('./')
from Huffman.huffman import huffman_compress
from Huffman.huffman import huffman_decompress
from Huffman.huffman import huffman_all_get_compressed
from Helper.run_and_time_func import run_and_time_function_1_2
from Helper.run_and_time_func import run_and_time_function_2_1

if __name__ == "__main__":

    file_name = "Katzen"

    # load LZ77 compressed file 
    file_path = "./files/LZ77/compressedImage_" + file_name + ".txt"
    flat_np_arr = np.fromfile(file_path, dtype=np.uint8)

    huffman_all_get_compressed(flat_np_arr)

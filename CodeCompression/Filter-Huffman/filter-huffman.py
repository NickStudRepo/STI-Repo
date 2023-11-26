import numpy as np
import sys

sys.path.append('./')
from Huffman.huffman import huffman_all_get_compressed

if __name__ == "__main__":

    file_name = "Katzen"

    # load LZ77 compressed file 
    file_path = "./files/LZ77/filteredImageBytes_" + file_name + ".txt"
    flat_np_arr = np.fromfile(file_path, dtype=np.uint8)

    huffman_all_get_compressed(flat_np_arr)

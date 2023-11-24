import numpy as np

# import local file
import sys
sys.path.append('./')
from ImageConversion.imageToNpArr import get_flat_np_arr_from_image
from ImageConversion.imageToNpArr import read_png_to_array

def lz77_compress(data, window_size, lookahead_buffer = 4):
    compressed_data = []
    i = 0
    print("Num of pixels: " + str(len(data)))
    while i < len(data):
        match = find_longest_match(data, i, window_size, lookahead_buffer)
        if match:
            length, distance = match
            compressed_data.append((length, distance))
            i += length
        else:
            compressed_data.append((0, data[i]))
            i += 1
        
        if i % 10 == 0:
            print("At pixel nr: " + i)

    return compressed_data

def find_longest_match(data, current_position, window_size, lookahead_buffer):

    end_of_buffer = min(current_position + lookahead_buffer, len(data) + 1)

    best_match_distance = -1
    best_match_length = -1

    # Optimization: Only consider substrings of length 2 and greater, and just 
    # output any substring of length 1 (8 bits uncompressed is better than 13 bits
    # for the flag, distance, and length)
    for j in range(current_position + 2, end_of_buffer):

        start_index = max(0, current_position - window_size)
        substring = data[current_position:j]

        for i in range(start_index, current_position):

            repetitions = len(substring) // (current_position - i)

            last = len(substring) % (current_position - i)

            matched_string = data[i:current_position] * repetitions + data[i:i+last]

            if matched_string == substring and len(substring) > best_match_length:
                best_match_distance = current_position - i 
                best_match_length = len(substring)

    if best_match_distance > 0 and best_match_length > 0:
        return (best_match_distance, best_match_length)
    return None


    # max_length = 0
    # best_distance = 0

    # print("here1")

    # end_of_buffer = min(current_index + lookahead_buffer, len(data) + 1)

    # for distance in range(current_index, end_of_buffer):

    #     start_index = max(0, current_index - window_size)
    #     # subarray = data[current_index:distance]
        
    #     for length in range(start_index,current_index):
            
    #         a = data[current_index:current_index + length]
    #         b = data[current_index - distance:current_index - distance + length]
    #         if (a == b).all():
    #             if length > max_length:
    #                 max_length = length
    #                 best_distance = distance

    # # for distance in range(1, min(current_index, window_size) + 1):
    # #     for length in range(1, min(len(data) - current_index, len(data) - distance)):
    # #         a = data[current_index:current_index + length]
    # #         b = data[current_index - distance:current_index - distance + length]
    # #         if (a == b).all():
    # #             if length > max_length:
    # #                 max_length = length
    # #                 best_distance = distance
    
    # print("here2")

    # return (max_length, best_distance) if max_length > 0 else None

def lz77_decompress(compressed_data):
    decompressed_data = []
    for item in compressed_data:
        length, distance = item
        if length == 0:
            decompressed_data.append(distance)
        else:
            start_index = len(decompressed_data) - distance
            for i in range(length):
                decompressed_data.append(decompressed_data[start_index + i])
    return np.array(decompressed_data)


if __name__ == "__main__":

    # flat_np_arr = get_flat_np_arr_from_image("reh", "ARW")
    # flat_np_arr = read_png_to_array("folie.png")

    # Example usage:
    flat_np_arr = np.array([1, 2, 3, 2, 3, 2, 3, 4, 1, 1, 2])

    window_size = 5  # Set your desired window size
    compressed_data = lz77_compress(flat_np_arr, window_size)
    decompressed_data = lz77_decompress(compressed_data)

    print("Original Data:", flat_np_arr)
    print("Compressed Data:", compressed_data)
    print("Decompressed Data:", decompressed_data)
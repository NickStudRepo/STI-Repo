import numpy as np
import warnings
import time

import sys
sys.path.append('./')
from LZ77.LZ77fast import LZ77Compressor
from Helper.run_and_time_func import run_and_time_function_2_1
from Helper.run_and_time_func import run_and_time_function_1_2
from Helper.run_and_time_func import print_time_infos
from ImageConversion.imageToNpArr import get_np_arr_from_image
from ImageConversion.imageToNpArr import read_png_to_matrix
from Huffman.huffman import huffman_all_get_compressed

# surpress Runtime overflow warnings
# Ignore the RuntimeWarning: overflow warning
warnings.filterwarnings("ignore", category=RuntimeWarning)

def apply_png_filter(image_array):
    channels, height, width = image_array.shape

    # Create an array for the filtered image
    filtered_array = np.zeros_like(image_array, dtype=np.uint8)
    filter_used = []

    # Apply the specified filter to each row and channel
    for c in range(channels):
        for y in range(height):
            channel_matrix = image_array[c,:,:]
            filter_type = choose_filter_type(channel_matrix, y)
            filter_used.append(filter_type)
            filtered_row = filter_row(channel_matrix, y, filter_type)
            filtered_array[c, y, :] = filtered_row

    return filtered_array, filter_used

def choose_filter_type(image_array, y):
    # Choose the filter type that minimizes the sum of absolute differences
    # filter_types = [filter_none, filter_sub, filter_up, filter_average, filter_paeth]
    filter_types = [0, 1, 2, 3, 4]

    score_of_filters = [0,0,0,0,0] # placeholders

    for filter in filter_types:
        filtered_row = filter_row(image_array, y, filter)
        # Remap values above 127 to 256 - original value
        remapped_arr = np.where(filtered_row > 127, filtered_row - 256, filtered_row)
        score_of_filters[filter] = np.sum(np.abs(remapped_arr))

    return np.argmin(score_of_filters)

def filter_row(channel_array, y, filter_type):
    width = channel_array.shape[1]

    # Apply the specified filter to each pixel in the row
    filtered_row = np.zeros_like(channel_array[y], dtype=np.int8)
    for x in range(width):
        filtered_row[x] = apply_filter(channel_array, x, y, filter_type)

    return filtered_row

def apply_filter(channel_array, x, y, filter_type):
    current_pixel = channel_array[y, x]
    previous_pixel = get_left_pixel(channel_array, x, y)
    above_pixel = get_above_pixel(channel_array, x, y)
    up_left_pixel = get_above_and_previous_pixel(channel_array, x, y)

    if filter_type == 0:  # None
        return current_pixel
    elif filter_type == 1:  # Sub
        return (current_pixel - previous_pixel) % 256
    elif filter_type == 2:  # Up
        return (current_pixel - above_pixel) % 256
    elif filter_type == 3:  # Average
        return (current_pixel - (int((previous_pixel + above_pixel) / 2))) % 256
    elif filter_type == 4:  # Paeth
        return (current_pixel - paeth_predictor(previous_pixel, above_pixel, up_left_pixel)) % 256
    else:
        raise ValueError("Invalid filter type")
    

def get_above_pixel(filtered_row, x, y):
    return 0 if y == 0 else filtered_row[y - 1, x]

def get_left_pixel(filtered_row, x, y):
    return 0 if x == 0 else filtered_row[y, x - 1]    

def get_above_and_previous_pixel(arr, x, y):
    # Check if the pixel above and to the left is within bounds
    if x > 0 and y > 0:
        return arr[y - 1, x - 1]
    else:
        return 0

def paeth_predictor(previous_pixel, above_pixel, up_left_pixel):
    v = previous_pixel + above_pixel - up_left_pixel
    vl = np.abs(v - previous_pixel)
    vu = np.abs(v - above_pixel)
    vul = np.abs(v - up_left_pixel)

    return min(vl, vu, vul)

#####################################################
# revert filtering

def revert_png_filter(filtered_array, filter_types):
    channels, height, width = filtered_array.shape
    original_array = np.zeros_like(filtered_array, dtype=np.uint8)

    # Revert the filtering for each row and channel
    for c in range(channels):
        for y in range(height):
            channel_matrix = filtered_array[c,:,:]
            original_row = revert_filter_row(channel_matrix, y, filter_types[c * height + y])
            original_array[c, y, :] = original_row

    return original_array

def revert_filter_row(channel_matrix, y, filter_type):
    width = len(channel_matrix[1])

    # Revert the specified filter for each pixel in the row
    reverted_row = np.zeros_like(channel_matrix[0,:], dtype=np.uint8)
    for x in range(width):
        reverted_pixel = revert_filter(channel_matrix, x, y, filter_type)
        channel_matrix[y,x] = reverted_pixel
        reverted_row[x] = reverted_pixel

    return reverted_row

def revert_filter(channel_matrix, x, y, filter_type):
    current_pixel = channel_matrix[y, x]
    above_pixel = get_above_pixel(channel_matrix, x, y)
    left_pixel = get_left_pixel(channel_matrix, x, y)
    above_and_left_pixel = get_above_and_previous_pixel(channel_matrix, x, y)

    if filter_type == 0:  # None
        return current_pixel
    elif filter_type == 1:  # Sub
        return (current_pixel + left_pixel) % 256
    elif filter_type == 2:  # Up
        return (current_pixel + above_pixel) % 256
    elif filter_type == 3:  # Average
        return (current_pixel + (int((left_pixel + above_pixel) / 2))) % 256
    elif filter_type == 4:  # Paeth
        return (current_pixel + paeth_predictor(left_pixel, above_pixel, above_and_left_pixel)) % 256
    else:
        raise ValueError("Invalid filter type")

##########################################


if __name__ == "__main__":
    
    image_name = "Katzen"
    image_type = ".png"
    file_name = image_name + image_type

    img_array = read_png_to_matrix(file_name)
    # img_array = get_np_arr_from_image("reh", "ARW")

    # filepaths 
    filtered_image_bytes = "./files/LZ77/filteredImageBytes_" + image_name + ".txt"
    compressed_filtered_image_bytes = "./files/LZ77/compressedFilteredImageBytes_" + image_name + ".txt"
    decompressed_filtered_image_bytes = "./files/LZ77/decompressedFilteredImageBytes_" + image_name + ".txt"
    filtered_image_filter_bytes = "./files/LZ77/filteredImageFilterBytes_" + image_name + ".txt"
    defiltered_image_bytes = "./files/LZ77/defilteredImageBytes_" + image_name + ".txt"

    # Time Filter application
    filtered_array, filter_used = run_and_time_function_1_2(apply_png_filter,img_array, "PNG Filtering")

    # write filtered array to file
    flat_array = filtered_array.flatten()
    flat_array.tofile(filtered_image_bytes)
    np.array(filter_used).tofile(filtered_image_filter_bytes)

    # sizes
    print("Size of original data: " + str(len(img_array.flatten())) + " Byte")
    print("Size of filtered data: " + str(len(flat_array)) + " Byte")
   
    # Time Revert Filter application
    reverted_array = run_and_time_function_2_1(revert_png_filter, filtered_array, filter_used, "Revert PNG Filtering")

    print("Size of reverted filters file: " + str(len(reverted_array.flatten())) + " Byte")

    # check if filters are equal
    print(np.array_equal(img_array, reverted_array))

    # LZ77
    compressor = LZ77Compressor(window_size=100)

	# LZ77 Kompression
    start_time = time.time()
    compressor.compress(filtered_image_bytes, output_file_path=compressed_filtered_image_bytes)
    finish_time = time.time()
    
    print_time_infos(start_time, finish_time, "LZ77 Kompression")

	# LZ77 Dekompression
    start_time = time.time()
    compressor.decompress(compressed_filtered_image_bytes, output_file_path=decompressed_filtered_image_bytes)
    finish_time = time.time()
    
    print_time_infos(start_time, finish_time, "LZ77 Dekompression")

    # Huffman
    flat_np_arr = np.fromfile(compressed_filtered_image_bytes, dtype=np.uint8)
    huffman_all_get_compressed(flat_np_arr)

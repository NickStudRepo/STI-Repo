import numpy as np
import time

import sys
sys.path.append('./')
from Helper.run_and_time_func import run_and_time_function_1_1
from ImageConversion.imageToNpArr import get_flat_np_arr_from_image
from ImageConversion.imageToNpArr import read_png_to_array

def run_length_encode(arr):
    # Ensure input is a NumPy array
    if not isinstance(arr, np.ndarray) or arr.ndim != 1:
        raise ValueError("Input must be a 1-dimensional NumPy array")
    
    encoded_data = []
    count = 1

    for i in range(1, len(arr)):
        if arr[i] == arr[i - 1]:
            count += 1
        else:
            encoded_data.append((arr[i - 1], count))
            count = 1
    
    # Handle the last element
    encoded_data.append((arr[-1], count))

    return np.array(encoded_data, dtype=[('value', arr.dtype), ('count', int)])

def run_length_decode(encoded_data):
    # Ensure input is a structured NumPy array with 'value' and 'count' fields
    if not isinstance(encoded_data, np.ndarray) or encoded_data.ndim != 1 or \
            'value' not in encoded_data.dtype.names or 'count' not in encoded_data.dtype.names:
        raise ValueError("Input must be a structured NumPy array with 'value' and 'count' fields")
    
    decoded_data = []

    for item in encoded_data:
        decoded_data.extend([item['value']] * item['count'])

    return np.array(decoded_data, dtype=encoded_data['value'].dtype)

def smallest_two_exponent(number):
    if number <= 0:
        raise ValueError("Input must be a positive number")
    x = 0
    power_of_two = 1
    while power_of_two <= number:
        power_of_two *= 2
        x += 1
    return x


if __name__ == "__main__":

    # original_array = get_flat_np_arr_from_image("reh", "ARW")
    original_array = read_png_to_array("Katzen.png")

    # RLE Kompression
    encoded_array = run_and_time_function_1_1(run_length_encode, original_array, "RLE Encoding")
    # RLE Dekompression
    decoded_array = run_and_time_function_1_1(run_length_decode, encoded_array, "RLE Decoding")

    original_array_size = len(original_array) 
    print("Original Image Size: " + str(original_array_size) + " Byte")

    # get max Runlength: 
    max_runlength = max(encoded_array, key=lambda x: x[1])[1]
    print("Max Runlenght: " + str(max_runlength))

    # how many bits to encode max runlength
    bits_for_max_runlength = smallest_two_exponent(max_runlength)
    print("Bits for max runlength: " + str(bits_for_max_runlength))
    # Filter the tuple_list for tuples with a second element above Threshhold
    threshhold = 16 # With 4 Bits you can represent ints from 1 to 16, including both
    filtered_tuples = [tup for tup in encoded_array if tup[1] > threshhold]

    # Annahme (value, Runlength), Value = 1 Byte, Runlength = 4 Bit -> Max Value: 16
    # + 0.5 Byte to tell the size of Bits of Runlength
    print(encoded_array.shape)
    encoded_array_size = len(encoded_array) * 1.5 + 0.5 

    original_array_size = len(original_array) 
    print("Original Image Size: " + str(original_array_size) + " Byte")

    print("Encoded Image Size: " + str(encoded_array_size) + " Byte")

    decoded_array_size = len(decoded_array)
    print("Decoded Image Size: " + str(decoded_array_size) + " Byte")


    # this is RLE with adaptive Runlength depending on max Runlength
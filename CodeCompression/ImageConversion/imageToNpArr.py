import rawpy
import imageio
import numpy as np


def get_flat_np_arr_from_image(file_name: str, file_type: str) -> np.array:

    base_input_path = './images/input/'
    image_path = base_input_path + file_name + "." + file_type

    # Read CR2 file using rawpy
    with rawpy.imread(image_path) as raw:
        # Perform demosaicing to obtain RGB image
        rgb_image = raw.postprocess()

    # Convert RGB image to NumPy array
    image_array = np.array(rgb_image)

    print("Original image shape: " + str(image_array.shape))
    flat_arr = image_array.flatten()
    print("Size of image / np array: " + str(len(flat_arr)) + " Byte")

    return flat_arr



if __name__ == "__main__":

    image_name = "reh"
    image_type = ".ARW"

    output_type = ".png"
    base_input_path = './images/input/'
    base_output_path = './images/output/'

    image_path = base_input_path + image_name + image_type
    output_path = base_output_path + image_name + output_type


    # Read CR2 file using rawpy
    with rawpy.imread(image_path) as raw:
        # Perform demosaicing to obtain RGB image
        rgb_image = raw.postprocess()

    # Convert RGB image to NumPy array
    image_array = np.array(rgb_image)
    # Convert raw data to a NumPy array
    print(image_array.shape)

    # work with np array
    flat_arr = image_array.flatten()
    print("Size of img: " + (len(flat_arr)) + " Byte") # 72721728 Byte


    # Now, image_array is a NumPy array containing the pixel values of your ARW image
    # Optionally, save the processed image as a common format (e.g., PNG)
    imageio.imwrite(output_path, image_array.astype(np.uint8))  




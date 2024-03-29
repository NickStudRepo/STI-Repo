import rawpy
import imageio
import numpy as np
from PIL import Image

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

    img_array = np.transpose(img_array, (2, 0, 1))
    print(str(img_array.shape))
    flat_arr = image_array.flatten()
    print("Size of image / np array: " + str(len(flat_arr)) + " Byte")

    return flat_arr

def get_np_arr_from_image(file_name: str, file_type: str) -> np.array:

    base_input_path = './images/input/'
    image_path = base_input_path + file_name + "." + file_type

    # Read CR2 file using rawpy
    with rawpy.imread(image_path) as raw:
        # Perform demosaicing to obtain RGB image
        rgb_image = raw.postprocess()

    # Convert RGB image to NumPy array
    image_array = np.array(rgb_image)

    print("Original image shape: " + str(image_array.shape))
    print("Size of image / np array: " + str(len(image_array.flatten())) + " Byte")

    img_array = np.transpose(img_array, (2, 0, 1))
    print(str(img_array.shape))

    return image_array


def read_png_to_array(file_name):
    file_path = './images/input/' + file_name
    # Open the PNG file
    img = Image.open(file_path)

    # Convert the image to RGB mode if it's not already
    img = img.convert("RGB")

    # Convert the image to a NumPy array
    img_array = np.array(img)
    print(str(img_array.shape))
    img_array = np.transpose(img_array, (2, 0, 1))
    print(str(img_array.shape))
    return img_array.flatten()

def read_png_to_matrix(file_name):
    file_path = './images/input/' + file_name
    # Open the PNG file
    img = Image.open(file_path)

    # Convert the image to RGB mode if it's not already
    img = img.convert("RGB")

    # Convert the image to a NumPy array
    img_array = np.array(img)
    print(str(img_array.shape))
    img_array = np.transpose(img_array, (2, 0, 1))
    print(str(img_array.shape))

    return img_array


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
    print("Size of img: " + str(len(flat_arr)) + " Byte") # 72721728 Byte


    # Now, image_array is a NumPy array containing the pixel values of your ARW image
    # Optionally, save the processed image as a common format (e.g., PNG)
    imageio.imwrite(output_path, image_array.astype(np.uint8))  




from PIL import Image
from wand.image import Image as Img
import pytesseract, os, cv2
import numpy as np


def get_text(path_to_file):
	if not path_to_file.endswith(".pdf"):
		print("Not a PDF file")
		return

	path_to_image = path_to_file[:-4] + ".jpg"

	with Img(filename=path_to_file) as img:
		img.compression_quality = 99
		img.save(filename=path_to_image)

	text = pytesseract.image_to_string(Image.open(path_to_image))
	#os.remove(path_to_image)
	return text


def get_text_preprocessing(path_to_file):
    if not path_to_file.endswith(".pdf"):
        print("Not a PDF file")
        return

    path_to_image = path_to_file[:-4] + ".jpg"

    with Img(filename=path_to_file) as img:
        img.compression_quality = 99
        img.save(filename=path_to_image)

    # Read image with opencv
    img = cv2.imread(path_to_image)

    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)

    #  Apply threshold to get image with only black and white
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

    # Write the image after apply opencv to do some ...
    cv2.imwrite(path_to_image, img)

    # Recognize text with tesseract for python
    text = pytesseract.image_to_string(Image.open(path_to_image))
    #os.remove(path_to_image)
    return text

# TODO: write text to file to be able to diff -y with solution
# TODO: write preprocessed images to file to see how clear they are
if __name__ == '__main__':
    test_path = './Testing/PDF_Files/test_pdf.pdf'
    print("=============================================")
    print(get_text(test_path))
    print("=============================================")
    print(get_text_preprocessing(test_path))
    print("=============================================")

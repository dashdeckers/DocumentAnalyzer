from PIL import Image
import pytesseract, os
from wand.image import Image as Img

def get_text(path_to_file):
	if not path_to_file.endswith(".pdf"):
		print("Not a PDF file")
		return

	path_to_image = path_to_file[:-4] + ".jpg"

	with Img(filename=path_to_file) as img:
		img.compression_quality = 99
		img.save(filename=path_to_image)

	text = pytesseract.image_to_string(Image.open(path_to_image))
	os.remove(path_to_image)
	return text
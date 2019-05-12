from PIL import Image
import pytesseract



from wand.image import Image as Img
with Img(filename='DavidCopperfield/onepage.pdf') as img: # , resolution=300
	img.compression_quality = 99
	img.save(filename='DavidCopperfield/onepage.jpg')

text = pytesseract.image_to_string(Image.open('DavidCopperfield/onepage.jpg'))
print(text)
'''
from tika import parser
raw = parser.from_file('sample2.pdf')
print(raw['content'])
'''
print("=================================================================================")


from PIL import Image
from wand.image import Image as Img
import pytesseract, os, cv2, json, string
import numpy as np
from spellchecker import SpellChecker


def get_text(path_to_file, preprocess=True):
    if not path_to_file.endswith(".pdf"):
        print("Not a PDF file")
        return

    path_to_image = path_to_file[:-4] + ".jpg"

    # Convert the pdf file to an image
    with Img(filename=path_to_file) as img:
        img.compression_quality = 99
        img.save(filename=path_to_image)

    # Preprocess the image
    if preprocess:
        # Read image with opencv
        img = cv2.imread(path_to_image)

        # Convert to gray
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply dilation and erosion to remove some noise
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)

        #  Apply threshold to get image with only black and white
        #img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

        # Write the image after apply opencv to do some ...
        cv2.imwrite(path_to_image, img)

    # Recognize text with tesseract
    text = pytesseract.image_to_string(Image.open(path_to_image))

    # Remove the image file, remove newlines from text, append newline to text
    os.remove(path_to_image)
    text = text.replace("\n", " ")
    text += "\n\n"

    # Write the text to a file
    path = os.path.join("Testing", "PDF_Files", "base_performance.txt")
    with open(path, 'w') as file:
        file.write(text)
    return text

# Get the strings read by the parsers
def get_attempts(verbose=False):
    test_path = './Testing/PDF_Files/test_pdf.pdf'
    base_performance = get_text(test_path, preprocess=False)
    preprocessed_performance = get_text(test_path)

    if verbose:
        print("=============================================")
        print(base_performance)
        print("=============================================")
        print(preprocessed_performance)
        print("=============================================")

    return [base_performance, preprocessed_performance]

# Get the solution string
def get_solution():
    solution_path = './Testing/PDF_Files/test_solution.txt'

    text = ""
    with open(solution_path, 'r') as file:
        for line in file:
            text += file.readline()
    return text

class Parser:
    def __init__(self, language='en'):
        if language in ['en', 'de', 'es', 'pt', 'fr']:
            self.spell = SpellChecker(language=language)
        elif len(language) == 2:
            path_to_dict_text = os.path.join(".", f"{language}_full.txt")
            path_to_dict = self.create_dictionary(path_to_dict_text)
            self.spell = SpellChecker(local_dictionary=path_to_dict)
        else:
            print("Language must be a valid two-letter language abbreviation")

        self.text = None
        self.tokens = None

    '''
    Create a frequency dictionary from a text file from the github:
    Provide a path to the .txt file containing two columns
    - words
    - frequencies
    This will create a .dict file which can be loaded by the spell-
    checker. It also returns the path to the .dict file
    '''
    def create_dictionary(self, filename, path="."):
        if not filename.endswith('.txt'):
            print("Must be a text file")
            return

        # Create the dictionary from the file
        freq_d = dict()
        full_path = os.path.join(path, filename)
        with open(full_path, 'r') as file:
            for line in file:
                tokens = line.split()
                freq_d[tokens[0]] = int(tokens[1])

        # Write the dictionary to a new file
        new_filename = filename[:-4] + '.dict'
        full_path = os.path.join(path, new_filename)
        with open(full_path, 'w') as file:
            file.write(json.dumps(freq_d))

        return full_path

    # Extract the text from a pdf file
    def extract_text(self, filename=None):
        if not filename:
            filename = './Testing/PDF_Files/test_pdf.pdf'
        self.text = get_text(filename)
        return self.text

    # Remove punctuation from- and tokenize the text
    def clean_text(self, extra_punctuation=""):
        if not self.text:
            print("Extract the text first before cleaning it!")
            return
        # Remove punctuation
        punctuation = string.punctuation + extra_punctuation + "—’"
        print("Punctuation:", punctuation)
        table = str.maketrans(dict.fromkeys(punctuation))
        self.text = self.text.translate(table)
        # Tokenize
        self.tokens = self.text.split()
        return self.tokens

    # Find the words in the text that are not in the dictionary
    def spellcheck(self):
        self.errors = self.spell.unknown(self.tokens)
        return self.errors

    # Show the context of the first (or all) occurance of a word in the text
    def show_context(self, word, context_range=3, show_all=False):
        if not self.tokens:
            print("Extract and clean the text first before looking for context!")
            return
        all_contexts = list()
        for idx, w in enumerate(self.tokens):
            # Found the word
            if w == word:
                # Get first and last indices
                first = idx - context_range
                last = idx + context_range + 1
                # Make sure they are not out of bounds
                if last > len(self.tokens) - 1:
                    last = len(self.tokens) - 1
                if first < 0:
                    first = 0
                # Show context
                context = self.tokens[first:last]
                print(context)
                # Either finish, or find all occurances
                if show_all:
                    all_contexts.append(context)
                else:
                    return context
        return all_contexts

    # Show the possible corrections of a word
    def show_corrections(self, word):
        options = self.spell.candidates(word)
        for idx, word in enumerate(options):
            # TODO: Show the options in the order of probability / distance
            print(f"[{idx}]\t{word}")
            if idx == 6:
                break
        print("[-1]\tNone of the above")
        return options

    # Replace all occurances of a word with the correction
    def correct_word(self, word, correction):
        # TODO: add option to correct all or only one occurance of the word
        if not self.tokens:
            print("Extract and clean the text first before correcting!")
        if correction == "Pick an option":
            print("Something went wrong, correction is definitely incorrect")
            return
        self.tokens[:] = [correction if w == word else w for w in self.tokens]


if __name__ == '__main__':
    spell = SpellChecker()

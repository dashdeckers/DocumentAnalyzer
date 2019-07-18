import PyPDF2, os, json, string
from spellchecker import SpellChecker

filename = "./Testing/PDF_Files/full.pdf"
filename1 = "./Testing/PDF_Files/test_pdf.pdf"
filename2 = "./Testing/Text_Files/Testing.txt"
dictfile = "./dict_50k.txt"

language_dict = {
    'english'   : 'en',
    'german'    : 'de',
    'spanish'   : 'es',
    'portuguese': 'pt',
    'french'    : 'fr',
    'en' : 'english',
    'de' : 'german',
    'es' : 'spanish',
    'pt' : 'portuguese',
    'fr' : 'french',
}

'''
Extracts text from a file.

TODO: Add support for .doc files

Returns None if something went wrong, otherwise the text as a string
'''
def text_extracter(filename=None):
    if not filename:
        print("No filename provided")
        return

    if filename.endswith('.pdf'):
        with open(filename, 'rb') as pdf:
            pdfreader = PyPDF2.PdfFileReader(pdf)
            # extract text per page
            full_text = ""
            for i in range(pdfreader.numPages):
                page_text = pdfreader.getPage(i).extractText()
                full_text += page_text
        # return full text
        return full_text

    if filename.endswith('.txt'):
        with open(filename, 'r') as textfile:
            text = textfile.read()
        return text

    print("Invalid file type")

'''
Create a frequency dictionary from a text file from the GitHub link

Provide a path to the .txt file containing two columns
- words
- frequencies

This will create a .dict file which can be loaded by the spell-
checker.

Returns the path to the .dict file as a string
'''
def create_dictionary(filename=None, path="."):
    if not (filename and filename.endswith('.txt')):
        print("Must be a text file")
        return

    if not os.path.exists(filename):
        print(f"File {filename} does not exist")
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

'''
Creates a SpellChecker object and handles language loading

Returns a SpellChecker object
'''
def create_spellchecker(language='en'):
    language = language.lower()
    if language in language_dict and len(language) != 2:
        language = language_dict[language]
    
    if language in ['en', 'de', 'es', 'pt', 'fr']:
        return SpellChecker(language=language)
    else:
        path_to_dict_text = os.path.join(".", f"{language}_full.txt")
        path_to_dict = create_dictionary(path_to_dict_text)
        if not path_to_dict:
            print(f'Did not find local dictionary for {language}')
            return
        return SpellChecker(local_dictionary=path_to_dict)

'''
Removes punctuation from a text

TODO: Parse again to remove stop words (which should come from a file?)

Returns cleaned text
'''
def clean_text(text=None, extra_punctuation=""):
    if not text:
        print("No text provided")
        return

    # Remove punctuation
    punctuation = string.punctuation + extra_punctuation + "Œ—•’‚˙˜˚ˆˇ˜Ł™˛˝˘"
    print("Punctuation to be removed:", punctuation)
    table = str.maketrans(dict.fromkeys(punctuation))
    text = text.translate(table)

    return text

'''
Show the context of the first (or all) occurance of a word in the text

Returns the context, or multiple contexts, as a list or list of lists
'''
def show_context(tokens=None, word=None, context_range=3, show_all=False):
    if not (tokens and isinstance(tokens, (list,))):
        print("No tokens provided")
        return

    if not word:
        print("No word provided")
        return

    all_contexts = list()
    for idx, w in enumerate(tokens):
        # Found the word
        if w == word:
            # Get first and last indices
            first = idx - context_range
            last = idx + context_range + 1
            # Make sure they are not out of bounds
            if last > len(tokens) - 1:
                last = len(tokens) - 1
            if first < 0:
                first = 0
            # Show context
            context = tokens[first:last]
            print(context)
            # Either finish, or find the rest
            if show_all:
                all_contexts.append(context)
            else:
                return context

    if len(all_contexts) == 0:
        print(f"No occurrances of the word {word} found")
        return

    return all_contexts

if __name__ == "__main__":
    #print(extract_text(filename2))
    #print(create_dictionary(dictfile))
    text = extract_text(filename)
    tokens = clean_text(text)
    print(" ".join(tokens))
    pass
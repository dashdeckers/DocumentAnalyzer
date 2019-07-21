from PyPDF2 import PdfFileReader
from json import dumps
from string import punctuation as string_punctuation
from os.path import join
from spellchecker import SpellChecker

file_folder = 'PDF_Files'
text_folder = 'Text_Files'

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

cat_infotext = '''These are the words that belong to the corresponding categories.
If you want to edit them directly: Then save the project, close the
program and open the corresponding text file located within the
project folder. This text file can be edited to add multiple words
to the wordlist directly, but make sure you put only one word per
line'''

filehist_infotext = '''This is the list of filenames that have already been extracted,
that means the text has been retrieved from the file, possibly edited and corrected,
and then saved. These filenames will be excluded from the extract step. To re-do
a file that is on this list: Close the program, open the file history text file
located within the project folder, remove that filename from the list, and then
save the file.
'''


def text_extracter(path_to_file=None):
    '''Extracts text from a pdf, doc or txt file.

    TODO: Add support for .doc files

    **Args**:

    * path_to_file (str): The path to the file to be processed

    **Returns**:
    The extracted text as a string, None if something went wrong.
    '''
    try:
        if not path_to_file:
            return

        if path_to_file.endswith('.pdf'):
            with open(path_to_file, 'rb') as pdf:
                pdfreader = PdfFileReader(pdf)
                full_text = ""
                for i in range(pdfreader.numPages):
                    page_text = pdfreader.getPage(i).extractText()
                    full_text += page_text
            return full_text

        if path_to_file.endswith('.txt'):
            with open(path_to_file, 'r') as textfile:
                text = textfile.read()
            return text

    except FileNotFoundError as e:
        print(f'File does not exists: {e}')

def create_dictionary(path_to_file=None):
    '''Create a frequency dictionary from a text file
    from the GitHub link below. This will create a
    .dict file which can be loaded by the spellchecker.

    hermitdave/FrequencyWords/tree/master/content/2016

    **Args**:

    * path_to_file (str): The path to a .txt file containing
    the columns (words, frequencies)

    **Returns**:
    A string containing the path to the .dict file
    '''
    try:
        if not path_to_file:
            return

        assert path_to_file.endswith('.txt'), 'Must be a text file'

        # Create the dictionary from the file
        freq_d = dict()
        full_path = join('.', path_to_file)
        with open(full_path, 'r') as file:
            for line in file:
                tokens = line.split()
                freq_d[tokens[0]] = int(tokens[1])

        # Write the dictionary to a new file
        new_path_to_file = path_to_file[:-4] + '.dict'
        full_path = join('.', new_path_to_file)
        with open(full_path, 'w') as file:
            file.write(dumps(freq_d))

        return full_path

    except FileNotFoundError as e:
        print(f'File does not exist: {e}')

    except AssertionError as e:
        print(e)

def create_spellchecker(language='en'):
    '''Creates a SpellChecker object

    **Args**:

    * language (str): The language that the spellchecker
    should be able to make corrections for

    **Returns** 
    A SpellChecker object
    '''
    language = language.lower()
    if language in language_dict and len(language) != 2:
        language = language_dict[language]
    
    if language in ['en', 'de', 'es', 'pt', 'fr']:
        return SpellChecker(language=language)

    else:
        path_to_dict_text = join(".", f"{language}_full.txt")
        path_to_dict = create_dictionary(path_to_dict_text)

        if not path_to_dict:
            print(f'Did not find local dictionary for {language}')
            return

        return SpellChecker(local_dictionary=path_to_dict)

def clean_text(text=None, extra_punctuation=""):
    '''Removes punctuation from the text and lowercases
    it. Currently removes:
    !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~Œ—•’‚˙˜˚ˆˇ˜Ł™˛˝˘

    **Args**:

    * text (str): The text to be cleaned

    * extra_punctuation (str): A string of punctuation marks
    to be removed that are not already included in 
    string.punctuation

    **Returns**:
    The cleaned text
    '''
    if not text:
        return

    punctuation = string_punctuation + extra_punctuation + "Œ—•’‚˙˜˚ˆˇ˜Ł™˛˝˘"
    table = str.maketrans(dict.fromkeys(punctuation))
    text = text.translate(table)

    return text.lower()

def get_context(tokens=None, word=None, context_range=2, show_all=False):
    '''Get the context of the first (or all) occurrence of a
    word in the tokenized text.

    **Args**:

    * tokens (list): The tokenized text.

    * word (str): The word to get the context of.

    * context_range (int): The number of words before and after
    the main word to retrieve.

    * show_all (bool): Whether or not to retrieve the context
    of all occurrences of the word.

    **Returns**
    The context, or multiple contexts, as a list of lists or a
    list of lists of lists.
    '''
    if not tokens or not word:
        return

    assert isinstance(tokens, (list,))

    all_contexts = list()
    for idx, w in enumerate(tokens):
        # Found the word
        if w == word:
            # Get first and last indices
            first = idx - context_range
            last = idx + context_range + 1
            # Make sure they are not out of bounds
            if last > len(tokens):
                last = len(tokens)
            if first < 0:
                first = 0
            # Get context
            context = tokens[first:last]
            context_split = [tokens[first:idx], tokens[idx+1:last]]
            # Either finish, or find the rest
            if show_all:
                all_contexts.append(context_split)
            else:
                return context_split

    return all_contexts

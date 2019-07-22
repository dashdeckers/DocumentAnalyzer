from PyPDF2 import PdfFileReader
from json import dumps
from string import punctuation as string_punctuation
from tkinter.ttk import Label
from DocumentAnalyzer.symspellpy.symspellpy import SymSpell

import os, sys

file_folder = 'PDF_Files'
text_folder = 'Text_Files'

language_dict = {
    'english' : 'en',
    'german'  : 'de',
    'dutch'   : 'nl',
    'en' : 'english',
    'de' : 'german',
    'nl' : 'dutch',
}

strings = {
    'default_text' : (
        '''Open or create a project via the menu to get started '''
    ),

    'cat_infotext' : (
        '''These are the words that belong to the corresponding categories.'''
        '''If you want to edit them directly: Then save the project, close '''
        '''the program and open the corresponding text file located within '''
        '''the project folder. This text file can be edited to add multiple '''
        '''words to the wordlist directly, but make sure you put only one '''
        '''word per line'''
    ),

    'filehist_infotext' : (
        '''This is the list of filenames that have already been extracted, '''
        '''that means the text has been retrieved from the file, possibly '''
        '''edited and corrected, and then saved. These filenames will be '''
        '''excluded from the extract step. To re-do a file that is on this '''
        '''list: Close the program, open the file history text file located '''
        '''within the project folder, remove that filename from the list, '''
        '''and then save the file.'''
    ),

    'p_name_err' : 'First line must start with "Project_name:"',
    'n_cats_err' : 'Second line must start with "Number_of_categories:"',
    'p_lang_err' : 'Third line must start with "Project_language:"',
    'blank_line_err'   : 'Fourth line must be emmpty',
    'folder_name_err'  : 'Folder name must be equal to the project name',

    'n_cat_lines_err' : (
        '''Number_of_categories not consistent with number of lines '''
        '''describing category names'''
    ),

    'n_cats_value_err'  : (
        '''Invalid "Number_of_categories" value in project info file.'''
        '''Must be an integer!'''
    ),

    'assertion_err' : lambda e: ( '''Problem with the project info file'''
        f'''structure: {e}.'''),

    'project_file_missing': (
        '''The project info file (project_info.txt) is missing.'''
        '''Is this a valid project folder?'''
    ),

    'cat_file_missing' : lambda e: f'A category file is missing: {e}.',

    'filehistory_missing' : lambda e: ('''The file history file is '''
        f'''missing: {e}.'''
    ),

    'broken_pipe_err' : 'Something weird happened, double check your work.',

    'filehist_inconsistency' : lambda inc_list: ('''There are files listed '''
         '''in the filehistory file that are not present in the files '''
        f'''folder: {[f for f in inc_list]}.'''
    ),

    'invalid_extension' : lambda inv_files: ('''File must be either pdf, '''
        f'''txt or doc. Skipping: {[f for f in inv_files]}.'''
    ),

    'invalid_name' : (
        '''Project name must be alphabetical, or with spaces, underscores'''
        '''or hyphens'''
    ),

    'invalid_language' : (
         '''Invalid language. Must be one of '''
        f'''{[l for l in list(language_dict.keys())]}'''
    ),

    'invalid_n_cats' : 'Number of categories must be an integer',
}

class WrappingLabel(Label):
    '''A Label that automatically adjusts the wrap to the window size'''
    def __init__(self, master=None, **kwargs):
        Label.__init__(self, master, **kwargs)
        self.bind('<Configure>',
                  lambda e: self.configure(wraplength=self.winfo_width() - 20))

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception as e:
        base_path = os.environ.get("_MEIPASS2", os.path.abspath("."))

    return os.path.join(base_path, relative_path)

def text_extracter(path_to_file=None):
    '''Extracts text from a pdf, doc or txt file.

    TODO: Add support for .doc files.

    **Args**:

    * path_to_file (str): The path to the file to be processed.

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

def create_spellchecker(language='en'):
    '''Creates a SpellChecker object.

    **Args**:

    * language (str): The language that the spellchecker
    should be able to make corrections for.

    **Returns** 
    A SpellChecker object, and
    None if something went wrong.
    '''
    if language.lower() in language_dict:
        language = language.lower()
        if len(language) > 2:
            language = language_dict[language]
    else:
        return

    spell = SymSpell()
    path_to_dict = os.path.join('Resources',
                                f'frequency_dictionary_{language}.txt')

    path_to_dict = resource_path(path_to_dict)

    if spell.load_dictionary(path_to_dict, 0, 1):
        return spell
    else:
        print(f'Could not find the dictionary.')
        return

def clean_text(text=None, extra_punctuation=""):
    '''Removes punctuation from the text and lowercases
    it. Currently removes:
    !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~Œ—•’‚˙˜˚ˆˇ˜Ł™˛˝˘

    **Args**:

    * text (str): The text to be cleaned.

    * extra_punctuation (str): A string of punctuation marks
    to be removed that are not already included in 
    string.punctuation.

    **Returns**:
    The cleaned text.
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
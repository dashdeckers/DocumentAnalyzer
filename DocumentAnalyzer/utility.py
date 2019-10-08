import re
import sys

from PyPDF2 import PdfFileReader
from tkinter.ttk import Label
from tkinter import Text, IntVar
from os import environ
from os.path import abspath, join

try:
    from DocumentAnalyzer.symspellpy.symspellpy import SymSpell
except ImportError as e:
    from symspellpy.symspellpy import SymSpell

file_folder = 'PDF_Files'
text_folder = 'Text_Files'

max_button_cols = 4

language_dict = {
    'english'    : 'en',
    'german'     : 'de',
    'dutch'      : 'nl',
    'hungarian'  : 'hu',
    'estonian'   : 'et',
    'lithuanian' : 'lt',
    'danish'     : 'da',
    'swedish'    : 'sv',
    'italian'    : 'it',

    'en' : 'english',
    'de' : 'german',
    'nl' : 'dutch',
    'hu' : 'hungarian',
    'et' : 'estonian',
    'lt' : 'lithuanian',
    'da' : 'danish',
    'sv' : 'swedish',
    'it' : 'italian',
}

class WrappingLabel(Label):
    '''A Label that automatically adjusts the wrap to the window size.
    '''
    def __init__(self, master=None, **kwargs):
        Label.__init__(self, master, **kwargs)
        self.bind('<Configure>',
                  lambda e: self.configure(wraplength=self.winfo_width() - 20))

class CustomText(Text):
    '''A text widget with two new methods, 
    tag_pattern() and
    delete_pattern()

    example:

    text = CustomText()
    text.tag_configure('red', foreground='#ff0000')
    text.tag_pattern('this should be red', 'red')
    text.delete_pattern('this should be deleted')

    The highlight_pattern method is a simplified python
    version of the tcl code at http://wiki.tcl.tk/3246
    '''
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)

    def tag_pattern(self, pattern, tag, start='1.0', end='end',
                    regexp=False):
        '''Apply the given tag to all text that matches the given pattern.
        '''
        task = 'tag'
        self._find_or_delete_pattern(pattern, task, tag, start, end, regexp)

    def delete_pattern(self, pattern, start='1.0', end='end',
                       regexp=False):
        '''Delete all text that matches the given pattern.
        '''
        task = 'delete'
        tag = None
        self._find_or_delete_pattern(pattern, task, tag, start, end, regexp)

    def _find_or_delete_pattern(self, pattern, task, tag=None, start='1.0',
                               end='end', regexp=False):

        assert task in ['tag', 'delete']

        start = self.index(start)
        end = self.index(end)
        self.mark_set('matchStart', start)
        self.mark_set('matchEnd', start)
        self.mark_set('searchLimit', end)

        count = IntVar()
        while True:
            index = self.search(pattern, 'matchEnd', 'searchLimit',
                                count=count, regexp=regexp)
            if index == '':
                break
            if count.get() == 0:
                break # degenerate pattern which matches zero-length strings
            self.mark_set('matchStart', index)
            self.mark_set('matchEnd', '%s+%sc' % (index, count.get()))
            if task == 'delete':
                self.delete('matchStart', 'matchEnd')
            else:
                self.tag_add(tag, 'matchStart', 'matchEnd')

def resource_path(relative_path):
    '''Get the absolute path to resource, works for dev and for PyInstaller.

    **Args**:

    * relative_path (str): The normal path to the file.

    **Returns**:
    The path to the file from a pyinstaller executable.
    '''
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception as e:
        base_path = environ.get('_MEIPASS2', abspath('.'))

    return join(base_path, relative_path)

def get_resource_paths(file):
    '''Get different possible paths to the resource file.

    **Args**:

    * file (str): The name of the file to be found in Resources/

    **Returns**:
    Three different possible paths to the file, depending on the working
    directory from which we are calling from or whether we are doing so
    from a pyinstaller executable.
    '''
    return [
        # Pyinstaller path
        resource_path(join('Resources', file)),
        # Top level path
        join('.', 'DocumentAnalyzer', 'Resources', file),
        # Module level path
        join('.', 'Resources', file),
    ]

def text_extracter(path_to_file=None):
    '''Extracts text from a pdf or txt file.

    TODO: Add support for .doc files.
    TODO: Do some minimal image pre-processing.

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
                full_text = ''
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

def clean_text(text=None):
    '''Removes all non-alphabetical characters except spaces
    from the text and lowercases it.

    **Args**:

    * text (str): The text to be cleaned.

    **Returns**:
    The cleaned text.
    '''
    if not text:
        return

    regex = re.compile('[^a-zA-Z \n]')
    text = regex.sub('', text)

    return text.lower()

def normalize_language(language):
    '''Converts a language input string to its two letter shortcut.
    If the language is not recognized or supported, return False.

    **Args**:

    * language (str): The string representing the language. Can be,
    for example, either 'English', 'english' or 'en'.

    **Returns**:
    The two letter shortcut, for example 'en'.
    '''
    if language.lower() in language_dict:
        language = language.lower()

        if len(language) > 2:
            language = language_dict[language]
        return language

    else:
        return False

def load_spellchecker(language, spellcheckers):
    '''Load a spellchecker from a pickle file and return it, unless we
    have already loaded it in which case return that one. If we created
    a new one, add it to the dictionary of spellcheckers. However, to
    keep from using up too much memory, at most 3 spellcheckers will be
    stored and the first added one will be removed.

    **Args**:

    * language (str): The language to load.

    * spellcheckers: A dictionary of already loaded spellcheckers.

    **Returns** 
    A SpellChecker object, and
    None if something went wrong.
    '''
    language = normalize_language(language)
    if not language:
        return

    if language in spellcheckers:
        return spellcheckers[language]

    if len(spellcheckers) > 2:
        # Remove the first added spellchecker if we already have 3
        del spellcheckers[list(spellcheckers.keys())[0]]

    spell = SymSpell()
    paths = get_resource_paths(f'fdist_{language}.txt')
    for path_to_fdist in paths:
        try:
            # Try loading the spellchecker and returning it
            if spell.load_dictionary(path_to_fdist, 0, 1):
                print(f'{path_to_fdist} worked!')
                spellcheckers[language] = spell
                return spell
            else:
                print(f'{path_to_fdist} did not work!')

        except FileNotFoundError:
            pass

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
                while len(context_split[0]) < context_range:
                    context_split[0].insert(0, '')
                while len(context_split[1]) < context_range:
                    context_split[1].append('')
                return context_split

    return all_contexts

strings = {
    'save_reminder' : lambda e: (
        f'''Do you want to {e.lower()}? Make sure to save the project '''
         '''first by synchronizing it!'''
    ),

    'delete_confirmation' : lambda e: (
        f'''Are you sure you want to delete every occurance of "{e}" from '''
        '''the text?'''
    ),

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
        '''Invalid "Number_of_categories" value in project info file. '''
        '''Must be an integer!'''
    ),

    'assertion_err' : lambda e: ( '''Problem with the project info file '''
        f'''structure: {e}.'''),

    'project_file_missing': (
        '''The project info file (project_info.txt) is missing. '''
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
        '''Project name must be alphabetical, or with spaces, underscores '''
        '''or hyphens'''
    ),

    'invalid_language' : (
         '''Invalid language. Must be one of '''
        f'''{[l for l in list(language_dict.keys())]}'''
    ),

    'invalid_n_cats' : 'Number of categories must be an integer',
}

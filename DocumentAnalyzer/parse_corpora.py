from nltk.probability import FreqDist
from lxml import etree
import os
import re
import time

def get_words_from_xml(path_to_xml, tag='w'):
    '''Parse the xml file containing a single language Europarl
    corpus, and return a preprocessed list of all the words in it.
    Preprocessing involves removing every non-alphabetical
    character from the word and lowercasing it.

    The corpora are available for download at:
    http://opus.nlpl.eu/Europarl.php

    **Args**:

    * path_to_xml (str): The path to the xml file.

    * tag (str): The tag to find, words are tagged with 'w'.

    **Returns**:
    A list of words, tokens if you will.
    '''
    with open(path_to_xml) as xmlfile:
        xml = xmlfile.read()

    regex = re.compile('[^a-zA-Z]')
    root = etree.fromstring(bytes(xml, 'utf-8'))

    words = list()
    for word in root.iter(tag):
        # Remove every non-alphabetical character and lowercase.
        clean_word = regex.sub('', word.text.lower())
        if clean_word:
            words.append(clean_word)

    return words

def get_fdist_of_language(lang='en', n_most_common=20000):
    '''Create a frequency distribution of a given language. Assumes
    that a single language Europarl corpus has been downloaded and
    lives in the same directory.

    The corpora are available for download at:
    http://opus.nlpl.eu/Europarl.php

    **Args**:

    * lang (str): A two letter language code representing the language
    to create a frequency distribution of, and coinciding with the name
    of the folder downloaded from the Europarl corpus website.

    * n_most_common (int): Number of most common words to include in the
    frequency distribution, so that you can trim the useless rest.

    **Returns**
    An nltk.probability.FreqDist object with the frequency distribution.
    '''
    path = os.path.join('DocumentAnalyzer', 'Resources', lang,
                        'Europarl', 'xml', lang)
    try:
        num_files = len(os.listdir(path))
    except FileNotFoundError as e:
        print(f'No {lang} file found in {path}!')
        return None

    t0 = time.time()
    all_words = list()
    for idx, filename in enumerate(os.listdir(path)):

        path_to_xml = os.path.join(path, filename)
        all_words.extend(get_words_from_xml(path_to_xml))

        print(f'File {idx+1}/{num_files} done in {time.time()-t0}')
        t0 = time.time()

    print(f'The language {lang} has {len(all_words)} words in total.')

    return FreqDist(all_words).most_common(n_most_common)

def write_fdist_to_file(fdist, lang='en'):
    '''Write a frequency distribution to file in the format 'word freq'.

    **Args**:

    * fdist (FreqDist): The frequency distribution to write to file.

    * lang (str): The two letter language code of the language of the
    frequency distribution.
    '''
    if fdist is None:
        return

    path = os.path.join('DocumentAnalyzer', 'Resources', f'fdist_{lang}.txt')
    with open(path, 'w') as file:
        for word, freq in fdist:
            file.write(f'{word} {freq}\n')

def process_all_corpora():
    '''Create a frequency distribution of each language in the language
    dictionary and write the results to file.
    '''
    for lang in language_dict:
        if len(lang) == 2:
            fdist = get_fdist_of_language(lang, 40000)
            write_fdist_to_file(fdist, lang)


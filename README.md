# Document Analyzer

## Usage

Simply download the .exe file and open it to get started.

### Create a project
Select the 'Create new project' option the 'Project' menu and specify the project name, language and number of categories (=wordlists). Then, specify the names of each of the categories.

### Open an existing project
Select the 'Open existing project' option in the 'Project' menu, then select a valid project folder.

### Saving the project
To save the project, select 'Synchronize current project' from the 'Project' menu. Synchronizing the project is a two way street, it combines what is contained in the files of the project folder and what is in the memory of the program. So synchronizing acts as both updating the program's knowledge from the contents of the files AND saving the program's knowledge to the files.

### Editing the project
Because synchronizing combines both the internal data and the file data into one, adding something to a file and then synchronizing the project is easy.\
\
However it is not possible to, for example, remove a word from a category by deleting it from the corresponding category file and then synchronizing the project. To remove data from the project, the program must first be closed. Then, entries can be deleted from the file and the program can be re-opened.

### The 'Extract Text' tab
This tab handles extracting text from the documents one by one, and editing them. Punctuation is removed in the extraction process, and all characters lowercased.\
\
Because extracting text from .pdf files is error-prone, the text is immediately spell checked and errors are highlighted. Clicking a spelling error will show a menu with some corrections, and clicking one of the corrections will replace the word, but the text can also be directly edited. The spell check can be re-run by selecting the 'Spellcheck' option in the 'Edit' menu.\
\
To save the text, select the 'Save & next document' option in the same menu. This will save the text as a .txt file in the 'Text_Files' folder under the same filename as the original file. The text can also be re-extracted to act as a reset in case of any severe mistakes by selecting 'Redo current document' in the 'Edit' menu.

### The 'Classify' tab
In this tab, words can be classified into one of the available categories either by clicking on the corresponding button or by pressing the corresponding number key. The words are shown in red, in the context that they appear in. The previous word and its context are shown above the current word and its context.\
\
Each word is classified only once, if the word should be in two or more categories then that must be done by adding the word to the category file manually.

### The 'Results' tab
Under construction.

### The 'Data View' tab
Here, the internal data can be viewed. Select a category or the 'File History' to see the what the contents of the selection, based on the internal program data. After synchronizing the project, those contents should be identical to the file contents.

## Project files

### Project folder structure
The project folder has a very specific structure:
```
Project_folder
└───PDF_Files
│   │   document1.pdf
│   │   document2.doc
│   │   document3.txt
│   │   ...
│
└───Text_Files
│   │   document1.txt
│   │   document2.txt
│   │   document3.txt
│   │   ...
│
│   project_info.txt
│   filehistory.txt
│   category1.txt
│   category2.txt
│   category3.txt
│   ...
```
The folder named 'PDF_Files' contains all the documents that you wish to analyze. The program currently supports .pdf, .doc and .txt file types.\
\
The folder named 'Text_files' will contain the text extracted from these documents in plain text (.txt) files, with the same file names as the original documents.\
\
The file 'project_info.txt' contains some information about the project such as the name, language, number of categories and the names of those categories.\
\
The file 'filehistory.txt' contains a list of file names that have already been extracted, so that the program knows that they can be skipped.\
\
These files can be edited, as long as they follow the rules listed below. After editing a file or adding or removing files from the 'PDF_Files' folders, the program needs to synchronize to see those changes. This is done by selecting the 'Synchronize current project' option in the 'Project' menu.

### Project file rules

The project_info.txt file must have the following structure:
```
Project_name: name
Number_of_categories: X
Project_language: language

Category_1_name: name
Category_2_name: name
```
The fields 'name', 'language' and 'X' can be changed. X must be an integer, and there must be just as many lines specifying category names as the value of X. Language can be either the two-letter shortcut (such as 'nl') or the full language name ('dutch'). Currently only Dutch, English and German are supported, but more can be added on request.\
\
The name of the project folder must be the same as the name of the project. The files in the 'PDF_Files' folder can be either .pdf, .doc or .txt files. The 'filehistory.txt' and the category files must contain only one word per line. There must be as many category files as the number of categories specified.


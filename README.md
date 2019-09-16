# Document Analyzer

## Getting started

### Installation

1. Download the file "DocumentAnalyzer_Installer.msi" and then run it on your computer to start the installation. Be aware that it might take a few minutes to load depending on your computer, this is due to the large language files necessary to do the spellchecking.

2. Agree to the the terms and conditions and optionally choose to create a desktop shortcut.

3. Important! When asked to choose a destination folder, pick a folder that you are familiar with because you will need to access it quite often. This is the folder in which your results will appear, and to which you will need to copy/move the pdf files that you wish to analyze.

4. Click install and wait for the installation to finish. The program, as well as the uninstall file, will now be located in the folder you specified.

### Usage

1. Open your file explorer and navigate to the folder you specified during the installation.

2. Open the program by double-clicking on it and create a new project using the drop down menu "Project", or use the keyboard shortcut "Ctrl + n". Be aware that the program might take a few minutes to open, depending on your computer.

3. In the pop-up window, provide the name of the project and choose a language from the drop down menu. This is the language that you expect the pdf files to be in, and the spellchecker will be set to that language for this project. Then, specify how many wordlists / categories you want your project to have and click "Create Project".

4. In the next pop-up window, give each wordlist / category a name and click "Done".

5. In the file explorer, you will notice that a new folder with the name of your project has appeared. Open that folder and copy the pdf files you wish to analyze into the folder names "PDF_Files".

6. In the program, refresh / synchronize the project using the drop down menu "Project", or use the keyboard shortcut "Ctrl + r". You should now see the attempted transcription of the first pdf file. Be aware that there will likely be many mistakes, unfortunately this cannot be avoided. You can edit this text file directly until it is correct, and you can use the spellchecker by clicking on a red underlined word. Re-run the spellchecker using the drop-down menu "Edit", or the keyboard shortcut "Ctrl + p". Once the text has been corrected, save the text using the drop-down menu "Edit" or the keyboard shortcut "Ctrl + s".

7. Saving the text will automatically transcribe the next pdf file. Once you are done extracting the text from the pdf files, you can click on the "Classify" tab to assign words to categories. In this tab, you will see a word highlighted in red, and the context in which it is in. Assign the word to one of the available categories by clicking on the name of the category, or by clicking on the corresponding number on the keyboard. Once a word has been assigned to a category, every subsequent occurance of the word will be skipped. If you wish to assign a word to two categories, you must open the text file in the project folder corresponding to the category name, type in the word manually, and save the file.

8. Don't forget to synchronize / refresh the project using the drop-down menu "Project", or the keyboard shortcut "Ctrl + r", to save your progress to the files in the project folder! This also updates the program to any changes made to those files directly (for example by adding a word to a category manually, as described in step 7).

9. Use the tabs "Results" and "View Data" to see the word counts for each category and the words assigned to each category, respectively. Synchronizing / refreshing your project will also write the newest results to the results.txt file which you can find in the project folder.


## More Details

### Create a project
Select the 'Create new project' option the 'Project' menu and specify the project name, language and number of categories (=wordlists). Then, specify the names of each of the categories.

### Open an existing project
Select the 'Open existing project' option in the 'Project' menu, then select a valid project folder. Note that project folders must be in the same directory as the program!

### Saving the project
To save the project, select 'Synchronize current project' from the 'Project' menu. Synchronizing the project is a two way street, it combines what is contained in the files of the project folder and what is in the memory of the program. So synchronizing acts as both updating the program's knowledge from the contents of the files AND saving the program's knowledge to the files.

### Editing the project
Because synchronizing combines both the internal data and the file data into one, adding something to a file and then synchronizing the project is easy.\
\
However it is not possible to, for example, remove a word from a category by deleting it from the corresponding category file and then synchronizing the project. To remove data from the project, the program must first be closed. Then, entries can be deleted from the file and the program can be re-opened. The same goes for re-transcribing a .pdf file by removing the filename from filehistory.txt: You can do this if you first close the program, then remove the filename from filehistory.txt, then re-open the program.

### The 'Extract Text' tab
This tab handles extracting text from the documents one by one, and editing them. Punctuation is removed in the extraction process, and all characters lowercased.\
\
Because extracting text from .pdf files is error-prone, the text is immediately spell-checked and errors are highlighted. Clicking a spelling error will show a menu with some corrections, and clicking one of the corrections will replace the word, but the text can also be directly edited. The spell check can be re-run by selecting the 'Spellcheck' option in the 'Edit' menu.\
\
To save the text, select the 'Save & next document' option in the same menu. This will save the text as a .txt file in the 'Text_Files' folder under the same filename as the original file. The text can also be re-extracted to act as a reset in case of any severe mistakes by selecting 'Redo current document' in the 'Edit' menu.

### The 'Classify' tab
In this tab, words can be classified into one of the available categories either by clicking on the corresponding button or by pressing the corresponding number key. The words are shown in red, in the context that they appear in. The previous word and its context are shown above the current word and its context.\
\
Each word is classified only once, if the word should be in two or more categories then that must be done by adding the word to the category file manually.

### The 'Results' tab
This tab shows the results, which are computed everytime the tab is opened. It goes through each word in all of the .txt files in the 'Text_Files' folder and then for each category, if that word appears in that category it increases the count for that category.

### The 'View Data' tab
Here, the internal data can be viewed. Select a category or the 'File History' to see the what the contents of the selection, based on the internal program data. After synchronizing the project, those contents will be identical to the file contents.

## Project files

### Project folder structure
The project folder has a very specific structure:
```
Project_folder
└───PDF_Files
│   │   document1.pdf
│   │   document2.txt
│   │   ...
│
└───Text_Files
│   │   document1.txt
│   │   document2.txt
│   │   ...
│
│   project_info.txt
│   filehistory.txt
|   results.txt
│   category1.txt
│   category2.txt
│   category3.txt
│   ...
```
The folder named 'PDF_Files' contains all the documents that you wish to analyze. The program currently supports .pdf and .txt file types.\
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
The fields 'name', 'language' and 'X' can be changed. X must be an integer, and there must be just as many lines specifying category names as the value of X. Language can be either the two-letter shortcut (such as 'nl') or the full language name ('dutch').\
\
The name of the project folder must be the same as the name of the project. The files in the 'PDF_Files' folder can be either .pdf or .txt files. The 'filehistory.txt' and the category files must contain only one word per line. There must be as many category files as the number of categories specified.


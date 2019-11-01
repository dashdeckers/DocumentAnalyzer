# Document Analyzer - User Manual

## Installation

1. Download the file "DocumentAnalyzer_Installer.msi" and then run it on your computer to start the installation. Be aware that it might take a few minutes to load depending on your computer.

2. Agree to the terms and conditions.

3. Important! When asked to choose a destination folder, pick a folder that you are familiar with because you will need to access it quite often. This is the folder in which your results will appear, and to which you will need to copy/move the PDF files that you wish to analyze.

4. Click install and wait for the installation to finish. The program, as well as the uninstall file, will now be located in the folder you specified.

## Usage

### Creating a project

1. Open your Windows file explorer and navigate to the folder you specified during the installation.

2. Open the program by double-clicking on it (keep in mind that it might take a while to open) and then click on the drop down menu "Project".

3. Click on "Create new project".

4. In the pop-up window, provide:
	- the name of the project,
	- the project language (this is the language that you expect the pdf files to be in), and
	- the number of categories (= wordlists) you want to have.
	Then click "Create Project".

5. In the next pop-up window, give each category a name and then click "Done".

6. In the file explorer, you will notice that a new folder with the name of your project has been created. That folder is your new project! We will call this your project folder from now on.

This folder contains a document for each of the categories you have created. These documents contain the words you assign to each category when you work on the project. The document “Project info” contains information on the project. The document “filehistory” is used by the program to make a record of the documents you have analysed in the project. See for more information below under Project Files.
Also, the folder contains two sub folders, one for the PDF files you will be analysing during the project, one for the converted Text files.


### Opening an existing project

1. Open your Windows file explorer and navigate to the folder you specified during the installation.

2. Open the program by double-clicking on it (keep in mind that it might take a while to open) and then click on the drop down menu "Project".

3. Click on "Open existing project".

4. In the pop-up window, select the project folder you want to open.

### Importing PDF files

1. Open your Windows file explorer and navigate to the project folder you want to import PDF files to.

2. Move or copy all the PDF files into the folder called "PDF_Files".

3. If the program was open during this time, then refresh it now by:
	- using the shortcut 'Control + s', or by
	- clicking the 'Synchronize current project' option in the 'Project' menu.

4. You should now see, in the text area, the program's attempt at transcribing the first PDF.

5. If you don't, close the program and open the file named 'filehistory.txt'. If every PDF file you have imported is listed in this file, then the program will think that you are done! Simply delete any (or every) of the PDF filenames from this file, then save it and re-open the program.

### Working on a project

In essence, working on a project requires three steps:

1. Transcribing PDF files to TEXT
	The program automatically transcribes PDF files to TEXT files. In doing so, it uses the standard word list of the language you have selected for the project. However, many mistakes in the transcription are bound to occur. 
Headers, page numbers and other formatting are removed from the text. 
The text files need to be checked before words can be classified. This is what the program prompts you to do first.

2. Assigning words to the categories
	After all the transcriptions of the PDF files have been checked, you can the words assign words to the categories. For automated assigning of words, you can import word lists to the documents for each category.

3. Results
	After all words have been assigned, the program will calculate the results. If you make changes to the word lists, the results need to be recalculated.

These steps are detailed below

### Correcting the text transcription and classifying words

1. Open or create a project as described above. 

2. Import some PDF files and make sure you see some transcribed text (also described above).

3. Edit this text until you are satisfied with the transcription, do this by:
	- editing the text directly, as you would a Word document,
	- using the spellchecker by clicking on a red-underlined word and then clicking on a suggested correction, and
	- using the 'Find and delete' option in the 'Edit' menu.

4. When you are done, save the text and transcribe the next PDF file, either by:
	- using the shortcut 'Control + n', or by
	- clicking on the 'Save & next document' option in the 'Edit' menu.
	You can view (and edit) these transcriptions in the Text_Files folder.

5. It is advised to open the PDF file in a window next to the program window. This way you can check the text document against the PDF file and remove redundant headers and footers if the program has not done this correctly. If not removed, the words in headers and footers will be classified and impact on the outcomes of the research. 

6. After you have finished transcribing the PDF files (or at any point beforehand), click on the 'Classify' tab.

Now assign each word to a category by clicking on the corresponding buttons or number keys on your keyboard. If you want to assign a word to two or more categories then assign it to one of the categories as described just now, then open the .txt file of the other category in your project folder and simply add the word to that list manually.

All words in the text files need to be assigned to a category. Words that are irrelevant for the research (e.g. verbs to be and have or stop words) need to be manually assigned to the ‘discard’ category the program automatically creates. Words that are difficult to assign can be temporarily stored in the category ‘discuss’. The words in this category can later be assigned to the correct category (or added to the ‘discard’ category.

Important! Save your progress by:
	- using the shortcut 'Control + s', or by
	- clicking the 'Synchronize current project' option in the 'Project' menu.
	The PDF transcriptions are saved every time you move to the next one (as described in step 4 above), but the **assigning of words to categories is only saved when you manually synchronize the project as described in this step.**

### Getting the results

1. While working on a project (as described above), every time you synchronize the project (manually, or by pressing 'Control + s') the most recent results are computed and saved.

2. For each category, you will find a corresponding CSV (= Excel) file in the project folder.

3. Open one of these CSV files and you will find the results in the following format:
	- Each row contains the frequencies of one of the words in that category.
	- Each column contains the frequencies of one of the PDF files.
	- Each cell contains the frequency of that particular word in that particular file.

4. To find out how often a word has occurred in total (across all PDFs), calculate the sum of the cells in that row.

5. To find out, across all PDFs, how often words of a certain category occur, sum all of the cells of that category.

6. Important! Everytime you make a change to a wordlist, be sure to synchronize the project ('Control + s') to update the results.

### Importing wordlists

The program creates word lists for each category in your project (plus the discard and discuss categories). You can import word list from another project to your current project by copy-pasting the words of each category into the appropriate category file in your new project as described below. Also, the word lists can be edited manually by typing words.

1. Navigate to the project folder of the project you want to update the wordlist of.

2. Open the category file corresponding to the wordlist you want to update. It will have a '.txt' extension, not '.csv'.

3. Copy the contents of your wordlist into this text file.

4. Important! You can edit this file as you please as long as there is only one word per line.


## More Details

### Saving the project
To save the project, select 'Synchronize current project' from the 'Project' menu. Synchronizing the project is a two way street, it combines what is contained in the files of the project folder and what is in the memory of the program. So synchronizing acts as both updating the program's knowledge from the contents of the files AND saving the program's knowledge to the files.

### Editing the project
Because synchronizing combines both the internal data and the file data into one, adding something to a file and then synchronizing the project is easy.\
\
However it is not possible to, for example, remove a word from a category by deleting it from the corresponding category file and then synchronizing the project. To remove data from the project, the program must first be closed. Then, entries can be deleted from the file and the program can be re-opened. The same goes for re-transcribing a .pdf file by removing the filename from filehistory.txt: You can do this if you first close the program, then remove the filename from filehistory.txt, then re-open the program.

### The 'Extract Text' tab
This tab handles extracting text from the documents one by one, and editing them. Punctuation is removed in the extraction process, and all characters lowercased.\
\
Because extracting text from .pdf files is error-prone, the text is immediately spell-checked and errors are highlighted. Clicking a spelling error will show a menu with some corrections, and clicking one of the corrections will replace the word, but the text can also be directly edited.\
\
To save the text, select the 'Save & next document' option in the same menu. This will save the text as a .txt file in the 'Text_Files' folder under the same filename as the original file. The text can also be re-extracted to act as a reset in case of any severe mistakes by selecting 'Redo current document' in the 'Edit' menu. If, after saving the text, you want to go back and edit it again you have two options: Either close the program, remove the filename of the file to edit from 'filehistory.txt' and then open the program again, or close the program and then edit the corresponding text file in the Text_Files folder using a different text editor.

### The 'Classify' tab
In this tab, words can be classified into one of the available categories either by clicking on the corresponding button or by pressing the corresponding number key. The words are shown in red, in the context that they appear in. The previous word and its context are shown above the current word and its context.\
\
Each word is classified only once, if the word should be in two or more categories then that must be done by adding the word to the category file manually.

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
│   all_words.txt
│   project_info.txt
│   filehistory.txt
│   category1.txt
│   category2.txt
│   category3.txt
│   ...
│   category1.csv
│   category2.csv
│   category3.csv
│   ...
```
The folder named 'PDF_Files' contains all the documents that you wish to analyze. The program currently supports .pdf and .txt file types.\
\
The folder named 'Text_files' will contain the text extracted from these documents in plain text (.txt) files, with the same file names as the original documents.\
\
The file 'all_words.txt' contains all the words from each wordlist, for convenience when looking up the location/existence of a word across wordlists.\
\
The file 'project_info.txt' contains some information about the project such as the name, language, number of categories and the names of those categories.\
\
The file 'filehistory.txt' contains a list of file names that have already been extracted, so that the program knows that they can be skipped.\
\
The 'categoryX.txt' files contain lists of words that belong to each of those categories.\
\
The 'categoryX.csv' files each contain an excel spreedsheet with the results for that category in the following format:
- each column represents one of the filenames
- each row represents one of the words in the wordlist
- each cell contains the number of occurrences for that word in that file\
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


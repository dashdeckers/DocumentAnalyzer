from DocumentAnalyzer.main import main

'''
Building on Windows:

> First use PyInstaller to create an executable file that bundles python:
- Open cmd
Win + R
cmd
- Go to the project directory
cd Document-Histograms
- Execute the PyInstaller command
pyinstaller --clean --onefile --noconsole --icon=doc.ico --name DocumentAnalyzer entrypoint.py
- Better to use the specfile in which we have specified the Resource folder
pyinstaller DocumentAnalyzer.spec

> Replace the .exe in project directory with the new .exe in the dist folder

> Use Inno Setup to create an installation executable from the app exe:
- Open the InnoSetup_Script.iss file with Inno Setup and compile

> Use MSI-Wrapper to create an MSI installer from the installation exe:
- Open MSI-Wrapper and use the configuration file or just do it normally

'''

if __name__ == '__main__':
    # from DocumentAnalyzer.utility import create_all_spellcheckers
    # create_all_spellcheckers()
	main()

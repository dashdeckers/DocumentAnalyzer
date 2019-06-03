import tkinter as tk
import tkinter.font as tkFont
import os

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # Define a font for the large create/choose project labels
        self.big_font = tkFont.Font(size=18, family="Times New Roman")

        # Finds existing projects and creates the options for the option menu
        self.create_option_menu()

        # Create all the options, show one of them
        self.create_new_project_options()
        self.create_existing_project_options()
        self.show_existing_project_options()

        # When the project selection changes, deal with that
        self.project_selection.trace("w", self.on_option_change)

        # Create next page button
        next_page = tk.Button(self,
                              text="Next Page",
                              width=20,
                              height=10,
                              command=self.on_next)
        next_page.grid(row=4, column=0, columnspan=2, sticky="s", pady=(100, 0))

        # Create error / info display
        self.error_text = tk.StringVar(self)
        error_display = tk.Label(self,
                                 textvariable=self.error_text,
                                 height=20)
        error_display.grid(row=5, column=0, columnspan=2, sticky="s")
        self.set_error_message("Info message")

    # Create the drop down menu to choose an existing project or a new one
    def create_option_menu(self):
        # Get the names of the project folders
        self.options = self.get_project_dir_names()
        self.options.append("Create a new project")
        # Create the variable to contain the choice, and set it to something
        self.project_selection = tk.StringVar(self)
        self.project_selection.set(self.options[0])
        # Create the text label
        choose_project = tk.Label(self,
                                  text="Choose a project:",
                                  font=self.big_font,
                                  width=20, 
                                  height=2)
        choose_project.grid(row=0, column=0)
        # Create the drop down menu
        popup_menu = tk.OptionMenu(self,
                                   self.project_selection,
                                   *self.options)
        popup_menu.config(width=25)
        popup_menu.grid(row=0, column=1)

    # Create all the options needed to create a new project
    def create_new_project_options(self):
        # TODO: Missing some options (language and # of cats)
        self.create_project = tk.Label(self,
                                       text="Project name:",
                                       font=self.big_font,
                                       width=20, 
                                       height=2)
        self.project_name = tk.Entry(self, width=25)

    # Show the create project options
    def show_new_project_options(self):
        self.create_project.grid(row=1, column=0)
        self.project_name.grid(row=1, column=1)

    # Hide the create project options
    def hide_new_project_options(self):
        self.create_project.grid_remove()
        self.project_name.grid_remove()

    # Create all the options needed to open an existing project
    def create_existing_project_options(self):
        self.clear_history = tk.IntVar(self)
        self.clear_h = tk.Checkbutton(self,
                                      variable=self.clear_history,
                                      text="Clear history")

        self.clear_cats = tk.IntVar(self)
        self.clear_c = tk.Checkbutton(self,
                                      variable=self.clear_cats,
                                      text="Clear cats")

    # Show the open existing project options
    def show_existing_project_options(self):
        self.clear_h.grid(row=2, column=0, columnspan=2)
        self.clear_c.grid(row=3, column=0, columnspan=2)

    # Hide the open existing project options
    def hide_existing_project_options(self):
        self.clear_c.grid_remove()
        self.clear_h.grid_remove()

    # When the user changes the drop down menu, possibly show/hide options
    def on_option_change(self, *args):
        if self.project_selection.get() == "Create a new project":
            self.hide_existing_project_options()
            self.show_new_project_options()
        else:
            self.hide_new_project_options()
            self.show_existing_project_options()

    # When the user hits the next page button, deal with that
    def on_next(self):
        from pdfpage import PDFPage
        selection = self.project_selection.get()
        name = self.project_name.get()
        if selection == "Create a new project" and name != "":
            if self.create_project_folder(name):
                self.master.switch_frame(PDFPage)
                return
        if selection != "Create a new project" and name == "":
            if self.open_project_folder(selection):
                self.master.switch_frame(PDFPage)
                return
        self.set_error_message("Options not set")

    # Sets the error message accordingly
    def set_error_message(self, error_type):
        if error_type == "Options not set":
            self.error_text.set(
                "To create a new project, choose the option\n"
                "from the drop down menu and provide a name.\n\n"
                "To open an existing project, choose the project\n"
                "from the drop down menu and leave the name blank.\n")
        if error_type == "Folder exists":
            self.error_text.set(
                "A folder with that name already exists, if it does not\n"
                "show up in the drop down menu, it does not conform to\n"
                "the project folder structure.")
        if error_type == "Info message":
            self.error_text.set(
                "Choose an existing project from the drop down menu\n"
                "above, or create a new one.\n"
                "You can modify the files in a project folder as you\n"
                "like, but don't delete any files or folders\n")

    # Open an existing project folder
    def open_project_folder(self, name):
        print("Opening an existing project: ", name)
        self.master.metadata['project_name'] = name
        if self.clear_history.get():
            print("-- Clearing history")
        if self.clear_cats.get():
            print("-- Clearing categories")
        return True

    # Create a new project folder
    def create_project_folder(self, name):
        # TODO: Make these options
        self.language = "English"
        self.num_cats = 1
        try:
            print("Creating a new project: ", name)
            pdir = os.path.join('.', name)
            os.mkdir(pdir)
            os.mkdir(os.path.join(pdir, 'PDF_Files'))
            os.mkdir(os.path.join(pdir, 'Text_Files'))
            for cat_num in range(1, self.num_cats + 1):
                with open(os.path.join(pdir, f'cat{cat_num}.txt'), 'w') as file:
                    file.write("")
            with open(os.path.join(pdir, 'project_info'), 'w') as file:
                file.write(f"Name: {name}\n")
                file.write(f"N_Cats: {self.num_cats}\n")
                file.write(f"Language: {self.language}\n")
            self.master.metadata['project_name'] = name
            self.master.metadata['n_categories'] = self.num_cats
            self.master.metadata['language'] = self.language
        except FileExistsError:
            self.set_error_message("Folder exists")
            return False
        return True

    # Returns the names of all project directories in the current directory
    def get_project_dir_names(self):
        d = '.'
        all_dirs = [os.path.join(d, o) for o in os.listdir(d)
                        if os.path.isdir(os.path.join(d, o))]

        p_dirs = [p_dir for p_dir in all_dirs if self.is_project_dir(p_dir)]
        return p_dirs

    # Checks if the provided directory contains a project based on whether the
    # two main folders and the project_info file exist within it
    def is_project_dir(self, p_dir):
        pdf = os.path.isdir(os.path.join(p_dir, 'PDF_Files'))
        txt = os.path.isdir(os.path.join(p_dir, 'Text_Files'))
        info = os.path.exists(os.path.join(p_dir, 'project_info'))
        return pdf and txt and info
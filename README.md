# Matthew Wilson
# Sprint 4 README
# Libary Usage
# sqlite3 for database creation, updating, pulling
# os and dotenv for storing/hiding/retrieving api key
# google.generativeai for communicating with Gemini AI
# markdown_pdf for transforming a markdown file to a pdf
# PySimpleGUI for gui creation and event handling
# Pytest to run tests on functions
#
# When running the application a GUI is opened that shows a list of jobs to choose from, a list of existing profiles to choose from, and the ability to create new profiles
# A job can be selected to show more information about the job, or the user can select a job and profile, and generate a personalized resume
# The resume will then be shown to the user, and they can choose to save the resume as a pdf to the project directory with a name of their choosing
# The bottom of the GUI window allows the user to create a new profile that will be saved to the database


# Sprint 3 README
# Libary Usage
# sqlite3 for database creation, updating, pulling
# PySimpleGUI for gui creation and event handling
# Pytest to run tests on functions
#
# When running the application the program connects to the database and ensures the personal_info table exists
# Then the GUI is generated and we grab all existing job titles via a sql query
# Any job can be highlighted and by clicking the 'select' button information about the job is generated on the right side of the GUI
# On the bottom of the GUI there are text boxes where information can be entered, and by clicking the 'Add' button, is saved to the database
# NOTE: personal_info table primary key is intended to auto increment as more entries are added, but populates with NULL values only


# Sprint 2 README
# Three libraries are used in this sprint
# The json library allows for the json files to be read into a list much easier
# The sqlite3 library allows for sql database creation/editing/querying etc
# The pytest library allows for easy function testing
#
# There is no direct interaction with this program past running it
# The program has two different methods to read a json file into a list of items based on the formatting of the objects in the file
# Then an empty database is created (or a connection to it is called if it already exists) with all the attributes that exist from our two json files
# Because these two json files have different attributes, we use two different functions to populate each into the sql database
# The changes are then saved into the database and it is closed
#

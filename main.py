import sqlite3
import PySimpleGUI as sg


# Full GUI layout with keys/event calls
def CreateGUI(jobs: list):
    layout = [
        [sg.vbottom(sg.Text('Available Jobs', font=('Arial', 16, 'bold'))), sg.Push(), sg.Column([
            [sg.Text('Job Description'), sg.Multiline(key='-JOB_DESC-', size=(70, 5), disabled=True)],
            [sg.Text('Company'), sg.InputText(key='-COMPANY-', size=(72, 1), readonly=True)],
            [sg.Text('Location'), sg.InputText(key='-LOCATION-', size=(72, 1), readonly=True)],
            [sg.Text('Pay Rate'), sg.InputText(key='-PAY-', disabled=True, size=(72, 1))],
            [sg.Text('Job Function'), sg.InputText(key='-FUNC-', disabled=True, size=(72, 1))]
        ], justification='right', element_justification='right')],

        [sg.Listbox(jobs, size=(40, 20), enable_events=True, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                    key='-LISTBOX-', horizontal_scroll=True)],

        [sg.Button('SELECT')],

        [sg.HorizontalSeparator(color='black', pad=(10, 10))],

        [sg.Text('Enter The Following Information and Click Add to Save Your Profile', font=('Arial', 16, 'bold'))],
        [sg.Text('*All Fields Must Contain a Value*', font=('Arial', 10, 'bold'))],
        [sg.Text('First Name'), sg.InputText(key='-FNAME-', size=(40, 1)), sg.Text('Last Name'), sg.InputText(key='-LNAME-', size=(40, 1))],
        [sg.Text('Email'), sg.InputText(key='-EMAIL-', size=(40, 1)), sg.Text('Phone Number'), sg.InputText(key='-PHONE-', size=(40, 1))],
        [sg.Text('Github URL'), sg.InputText(key='-GIT-', size=(40, 1)), sg.Text('Classes Taken'), sg.InputText(key='-CLASSES-', size=(40, 1))],
        [sg.Text('Projects'), sg.Multiline(key='-PROJECTS-', size=(40, 6)), sg.Text('Other Info'), sg.Multiline(key='-INFO-', size=(40, 6))],
        [sg.Button('Add')],
        [sg.StatusBar(key='-STATUS-', text='', size=(100, 1))]
    ]

    # Apply layout to GUI and open
    window = sg.Window('Job Database', layout, size=(1200, 1000))

    # While open check if window is closed and for events
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == 'SELECT':
            print('Row Chosen', window['-LISTBOX-'].get_indexes())
            index = window['-LISTBOX-'].get_indexes()

            job_description = SQL_Search('description', index, cursor)
            window['-JOB_DESC-'].update(job_description)

            company = SQL_Search('company', index, cursor)
            window['-COMPANY-'].update(company)

            location = SQL_Search('location', index, cursor)
            window['-LOCATION-'].update(location)

            pay = SQL_Search('salary_range, interval, min_amount, max_amount', index, cursor)
            window['-PAY-'].update(pay)

            job_func = SQL_Search('job_function', index, cursor)
            window['-FUNC-'].update(job_func)

        if event == 'Add':
            info_list = [window['-FNAME-'].get(), window['-LNAME-'].get(), window['-EMAIL-'].get(),
                         window['-PHONE-'].get(), window['-GIT-'].get(), window['-CLASSES-'].get(),
                         window['-PROJECTS-'].get(), window['-INFO-'].get()]
            print(info_list)
            if check_empty_string(info_list) == True:
                window['-STATUS-'].update('Profile NOT Added, Please Ensure No Fields Are Left Empty')
                info_list.clear()
            else:
                SQL_Add(info_list, cursor)
                info_list.clear()
                window['-FNAME-'].update(""), window['-LNAME-'].update(""), window['-EMAIL-'].update(""),
                window['-PHONE-'].update(""), window['-GIT-'].update(""), window['-CLASSES-'].update(""),
                window['-PROJECTS-'].update(""), window['-INFO-'].update("")
                window['-STATUS-'].update('Profile Added to Database')

    window.close()


# Check if any strings were left empty
def check_empty_string(string_list: list):
    for i in string_list:
        if i == '':
            return True
    return False


# Table creation for personal info
def create_personal_info_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS personal_info (
    ID INTEGER PRIMARY KEY AUTOINCREMENT not null,
    First_Name VARCHAR(30),
    Last_Name VARCHAR(30),
    Email VARCHAR(100),
    Phone_Number VARCHAR(15),
    Github_Link VARCHAR(100),
    Projects VARCHAR(255),
    Classes VARCHAR(255),
    Personal_Info VARCHAR(255)
    )
    ''')


# Searches database for given attribute by row id
# row id must be incremented by 1, as SQL database begins at 1
def SQL_Search(column_name: str, row_id: tuple, cursor):
    query = f"SELECT {column_name} FROM jobs WHERE rowid = ?"
    index = list(row_id)
    index[0] += 1
    row_tuple = tuple(index)
    return list(cursor.execute(query, row_tuple))


# Add personal info to table
def SQL_Add(info_list: list, cursor):
    insert_statement = ('INSERT INTO personal_info (First_Name, Last_Name, Email, Phone_Number, Github_Link, Projects,'
                        ' Classes, Personal_Info) VALUES(?, ?, ?, ?, ?, ?, ?, ?)')
    try:
        cursor.execute(insert_statement, info_list)
    except sqlite3.Error:
        print('Do Not Leave Any Attributes Empty')


# Save close database, *always run this at end of main*
def save_database():
    connection.commit()
    connection.close()


if __name__ == '__main__':

    connection = sqlite3.connect('job_ads.db')
    cursor = connection.cursor()

    create_personal_info_table()

    job_titles = list(cursor.execute('Select title FROM jobs'))
    CreateGUI(job_titles)

    save_database()

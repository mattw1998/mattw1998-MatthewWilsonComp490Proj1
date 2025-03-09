import sqlite3
import PySimpleGUI as sg
import google.generativeai as genai
import os
from dotenv import load_dotenv, find_dotenv
from markdown_pdf import MarkdownPdf
from markdown_pdf import Section


# Full GUI layout with keys/event calls
def Create_GUI(jobs: list, profiles: list, cursor):
    layout = [
        [sg.vbottom(sg.Text('Available Jobs', font=('Arial', 16, 'bold'))), sg.Push(), sg.Column([
            [sg.vtop(sg.Text('Job Description')), sg.Multiline(key='-JOB_DESC-', size=(70, 5), disabled=True)],
            [sg.Text('Company'), sg.InputText(key='-COMPANY-', size=(72, 1), readonly=True)],
            [sg.Text('Location'), sg.InputText(key='-LOCATION-', size=(72, 1), readonly=True)],
            [sg.Text('Pay Rate'), sg.InputText(key='-PAY-', disabled=True, size=(72, 1))],
            [sg.Text('Job Function'), sg.InputText(key='-FUNC-', disabled=True, size=(72, 1))]
        ], justification='right', element_justification='right')],

        [sg.Listbox(jobs, size=(50, 15), enable_events=True, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                    key='-JOBLISTBOX-', horizontal_scroll=True), sg.Push(), sg.vtop(sg.Text('Choose A Profile')),
         sg.vtop(sg.Listbox(profiles, size=(30, 5), enable_events=True, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE,
                            key='-PROFILELISTBOX-'))],

        [sg.Button('SELECT'), sg.Push(), sg.Text('Select desired job/profile and click the button to generate a resume'), sg.Button('Generate')],

        [sg.Push(), sg.vtop(sg.Text('Generated Resume')), sg.Multiline(key='-RESUME-', size=(60, 8), disabled=True)],

        [sg.Push(), sg.Text('Enter a file name and click save to save the file as a PDF'),
         sg.InputText(key='-FILENAME-', size=(25, 1)), sg.Text('.pdf', font=('Arial', 10, 'italic')), sg.Button('SAVE')],

        [sg.HorizontalSeparator(color='black', pad=(5, 5))],

        [sg.Text('Enter The Following Information and Click Add to Save Your Profile', font=('Arial', 16, 'bold'))],
        [sg.Text('*All Fields Must Contain a Value*', font=('Arial', 10, 'bold'))],
        [sg.Text('Profile Name'), sg.InputText(key='-PROFILE-', size=(30, 1)), sg.Text('First Name'), sg.InputText(key='-FNAME-', size=(30, 1)), sg.Text('Last Name'), sg.InputText(key='-LNAME-', size=(30, 1))],
        [sg.Text('Email'), sg.InputText(key='-EMAIL-', size=(40, 1)), sg.Text('Phone Number'), sg.InputText(key='-PHONE-', size=(40, 1))],
        [sg.Text('Github URL'), sg.InputText(key='-GIT-', size=(50, 1)), sg.Text('Classes Taken'), sg.InputText(key='-CLASSES-', size=(60, 1))],
        [sg.vtop(sg.Text('Projects')), sg.Multiline(key='-PROJECTS-', size=(50, 5)), sg.vtop(sg.Text('Other Info')), sg.Multiline(key='-INFO-', size=(50, 5))],
        [sg.Button('Add')],

        [sg.vbottom(sg.StatusBar(key='-STATUS-', text='', size=(250, 1)))]
    ]

    # Apply layout to GUI and open
    window = sg.Window('Job Database', layout, size=(1200, 1000))

    # While open check if window is closed and for events
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        # Shows job information
        if event == 'SELECT':
            try:
                # Get index of selected job
                index = window['-JOBLISTBOX-'].get_indexes()

                # sql queries for job information
                job_description = SQL_Job_Search('description', index, cursor)
                window['-JOB_DESC-'].update(job_description)

                company = SQL_Job_Search('company', index, cursor)
                window['-COMPANY-'].update(company)

                location = SQL_Job_Search('location', index, cursor)
                window['-LOCATION-'].update(location)

                pay = SQL_Job_Search('salary_range, interval, min_amount, max_amount', index, cursor)
                window['-PAY-'].update(pay)

                job_func = SQL_Job_Search('job_function', index, cursor)
                window['-FUNC-'].update(job_func)

            except IndexError:
                window['-STATUS-'].update('Please Choose A Job From The List Before Clicking, "SELECT"')

        # Add profile to database
        if event == 'Add':
            info_list = [window['-PROFILE-'].get(), window['-FNAME-'].get(), window['-LNAME-'].get(), window['-EMAIL-'].get(),
                         window['-PHONE-'].get(), window['-GIT-'].get(), window['-PROJECTS-'].get(),
                         window['-CLASSES-'].get(), window['-INFO-'].get()]

            # Check all boxes contain text
            if check_empty_string(info_list) == True:
                window['-STATUS-'].update('Profile NOT Added, Please Ensure No Fields Are Left Empty')
                info_list.clear()

            # Check for duplicate profile names
            elif check_profile_exists(info_list[0], cursor) == True:
                window['-STATUS-'].update('Profile NOT Added, Please Choose A Unique Profile Name')
                info_list.clear()

            else:
                SQL_Add(info_list, cursor)
                connection.commit()
                info_list.clear()
                window['-PROFILE-'].update(""), window['-FNAME-'].update(""), window['-LNAME-'].update(""),
                window['-EMAIL-'].update(""), window['-PHONE-'].update(""), window['-GIT-'].update(""),
                window['-CLASSES-'].update(""), window['-PROJECTS-'].update(""), window['-INFO-'].update("")
                window['-STATUS-'].update('Profile Added to Database')
                window['-PROFILELISTBOX-'].update(Refresh_Profile_List(cursor))

        # Send query to LLM to create job resume
        if event == 'Generate':
            # Create empty lists to populate table info into
            job_info = []
            profile_info = []

            job_index = window['-JOBLISTBOX-'].get_indexes()
            job_info.append(list(SQL_Job_Search('title', job_index, cursor)))
            job_info.append(list(SQL_Job_Search('description', job_index, cursor)))
            job_info_fix = Fix_SQL_Return_Strings(job_info)

            profile_index = window['-PROFILELISTBOX-'].get_indexes()
            profile_info.append(list(SQL_Profile_Search('First_Name', profile_index, cursor)))
            profile_info.append(list(SQL_Profile_Search('Last_Name', profile_index, cursor)))
            profile_info.append(list(SQL_Profile_Search('Github_Link', profile_index, cursor)))
            profile_info.append(list(SQL_Profile_Search('Projects', profile_index, cursor)))
            profile_info.append(list(SQL_Profile_Search('Classes', profile_index, cursor)))
            profile_info.append(list(SQL_Profile_Search('Personal_Info', profile_index, cursor)))
            profile_info.append(list(SQL_Profile_Search('Email', profile_index, cursor)))
            profile_info.append(list(SQL_Profile_Search('Phone_Number', profile_index, cursor)))
            profile_info_fix = Fix_SQL_Return_Strings(profile_info)


            # Query LLM and create markdown file with resume
            cover_letter, resume = Query_LLM(job=job_info_fix, profile=profile_info_fix, model=model)
            Create_MD_File(cover_letter, resume)

            window['-RESUME-'].update("")
            window['-RESUME-'].update(f"{cover_letter} \n\n\n {resume}")

            # Empty lists after use
            job_info.clear()
            job_info_fix.clear()
            profile_info.clear()
            profile_info_fix.clear()

        # Save resume as PDF
        if event == 'SAVE':
            try:
                file_name = window['-FILENAME-'].get()
                if file_name == "":
                    window['-STATUS-'].update('Please Enter A File Name Before Saving')
                else:
                    if Check_File_Exists(file_name) == True:
                        window['-STATUS-'].update('Please Choose A Unique File Name')
                    else:
                        Markdown_To_PDF(file_name)
            except FileNotFoundError:
                window['-STATUS-'].update('You Must First Generate A Resume Before Trying To Save')
            except OSError:
                window['-STATUS-'].update('Please Enter A Valid File Name (alphanumeric characters only)')

    window.close()


# Check for empty strings in list
def check_empty_string(string_list: list):
    for i in string_list:
        if i == '':
            return True
    return False


# Check if username already exists (not case-sensitive)
def check_profile_exists(profile_name, cursor):
    profiles = list(cursor.execute('SELECT Profile_Name FROM personal_info'))
    for existing_name in profiles:
        if profile_name.lower() == str(existing_name).lower():
            return True
    return False


# Table creation for personal info
def create_personal_info_table(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS personal_info (
    Profile_Name VARCHAR(20) PRIMARY KEY not null,
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


# Searches job table for given attribute by row id
# row id must be incremented by 1, as SQL database begins at 1
def SQL_Job_Search(column_name: str, row_id: tuple, cursor):
    query = f"SELECT {column_name} FROM jobs WHERE rowid = ?"
    index = list(row_id)
    index[0] += 1
    row_tuple = tuple(index)
    return list(cursor.execute(query, row_tuple))


# Searches profile table for given attribute by row id
# row id must be incremented by 1, as SQL database begins at 1
def SQL_Profile_Search(column_name: str, row_id: tuple, cursor):
    query = f"SELECT {column_name} FROM personal_info WHERE rowid = ?"
    index = list(row_id)
    index[0] += 1
    row_tuple = tuple(index)
    return list(cursor.execute(query, row_tuple))


# Add personal info to table
def SQL_Add(info_list: list, cursor):
    insert_statement = ('INSERT INTO personal_info (Profile_Name, First_Name, Last_Name, Email, Phone_Number,'
                        ' Github_Link, Projects, Classes, Personal_Info) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)')
    try:
        cursor.execute(insert_statement, info_list)
    except sqlite3.Error:
        print('Do Not Leave Any Attributes Empty')


# Removes junk from beginning/end of strings returned from SQL queries
def Fix_SQL_Return_Strings(list):
    new_list = []
    for i in list:
        new_list.append(str(i)[3:-4])
    return new_list


def Refresh_Profile_List(cursor):
    return list(cursor.execute('SELECT Profile_Name FROM personal_info ORDER BY rowid'))


# Setup gemini ai w/ API key
def Configure_LLM():
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    API_KEY = os.getenv("key")
    # configure gemini AI w/ api key
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    return model


def Query_LLM(job: list, profile: list, model):
    query = (f"Return me a brief cover letter for a resume in markdown format including, my name {profile[0]} "
             f"{profile[1]}, my Github url {profile[2]}, my email {profile[6]}, and my phone number {profile[7]}")
    cover_letter = model.generate_content(query)

    query = (f"Return me a body for a job resume in markdown format based only on the following job description and personal "
             f"information provided to you. The job title is {job[0]}, with the description, {job[1]}. My notable "
             f"projects completed are: {profile[3]}. The classes I have taken are: {profile[4]}. Other information that"
             f" should be included: {profile[5]}.")
    resume = model.generate_content(query)
    return cover_letter.text, resume.text


# Takes string input and creates markdown file
def Create_MD_File(cover_letter: str, resume: str):
    with open('cover_letter.md', 'w') as file:
        file.write(cover_letter)
    with open('resume.md', 'w') as file:
        file.write(resume)


# Converts Markdown to PDF (Markdown file name can be entered statically as it is auto names in 'Create_MD_File' function)
def Markdown_To_PDF(file_name: str):
    with open('cover_letter.md', 'r') as file:
        heading = file.read()
    with open('resume.md', 'r') as file:
        body = file.read()

    pdf = MarkdownPdf(toc_level=1)
    pdf.add_section(Section(heading))
    pdf.add_section(Section(body))
    pdf.save(f"{file_name}.pdf")


def Check_File_Exists(file_name):
    if os.path.exists(f"{file_name}.pdf"):
        return True
    else:
        return False


# Save close database, *always run this at end of main*
def Save_Database():
    connection.commit()
    connection.close()


if __name__ == '__main__':
    model = Configure_LLM()
    connection = sqlite3.connect('job_ads.db')
    cursor = connection.cursor()

    create_personal_info_table(cursor)

    job_titles = list(cursor.execute('Select title FROM jobs'))
    profiles = list(cursor.execute('SELECT Profile_Name FROM personal_info ORDER BY rowid'))
    Create_GUI(job_titles, profiles, cursor)

    Save_Database()

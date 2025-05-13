import sqlite3
import PySimpleGUI as Sg
import google.generativeai as genai
import os
from dotenv import load_dotenv, find_dotenv
from markdown_pdf import MarkdownPdf
from markdown_pdf import Section
from functions import *



if __name__ == '__main__':
    model = Configure_LLM()
    connection = sqlite3.connect('job_ads.db')
    cursor = connection.cursor()

    create_personal_info_table(cursor)

    job_titles = list(cursor.execute('Select title FROM jobs'))
    profiles = list(
        cursor.execute('SELECT Profile_Name FROM personal_info ORDER BY rowid')
    )
    Create_GUI(job_titles, profiles, cursor, connection, model)

    Save_Database(connection)

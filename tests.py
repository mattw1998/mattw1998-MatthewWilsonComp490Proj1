import pytest
import main
import sqlite3
import os
from dotenv import load_dotenv, find_dotenv
import requests


def test_SQL_Add():
    connection = sqlite3.connect('job_ads.db')
    cursor = connection.cursor()
    main.SQL_Add(['1', '2', '3', '4', '5', '6', '7', '8', '9'], cursor)
    query = "SELECT * FROM personal_info ORDER BY rowid DESC LIMIT 1"
    result = list(cursor.execute(query))
    assert result == [('1', '2', '3', '4', '5', '6', '7', '8', '9')]
    main.SQL_Add(['doug', 'doug', 'douglas', 'doug@gmail.com', '12345', '111222333', 'aa', 'aa', 'aa'], cursor)
    result = list(cursor.execute(query))
    assert result == [('doug', 'doug', 'douglas', 'doug@gmail.com', '12345', '111222333', 'aa', 'aa', 'aa')]


def test_SQL_Search():
    connection = sqlite3.connect('job_ads.db')
    cursor = connection.cursor()
    assert list(main.SQL_Job_Search('id', (0,), cursor)) == [('s-GCjOL5C9JmbOP8AAAAAA==',)]
    assert (list(main.SQL_Job_Search('title', (4,), cursor)) ==
            [('Senior Software Development Engineer',)])


# setup for requests.post taken and edited from Google Gemini
# tests that api key is returning 200 http response code
def test_LLM_HTTP_Reponse():
    dotenv_path = find_dotenv()
    load_dotenv(dotenv_path)
    API_KEY = os.getenv("key")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY,
    }
    payload = {
        # Your request payload here
        "contents": [{
            "parts": [{
                "text": "TEST"
            }]
        }]
    }
    response = requests.post(url, headers=headers, json=payload)
    assert response.status_code == 200


def test_Resume_Contains_Keywords():
    connection = sqlite3.connect('job_ads.db')
    cursor = connection.cursor()
    model = main.Configure_LLM()

    # Setup test job and profile for resume query
    job = []
    job.append(main.SQL_Job_Search('title', (1,), cursor))
    job.append(main.SQL_Job_Search('description', (1,), cursor))
    new_job = main.Fix_SQL_Return_Strings(job)

    profile = []
    profile.append(list(main.SQL_Profile_Search('First_Name', (0,), cursor)))
    profile.append(list(main.SQL_Profile_Search('Last_Name', (0,), cursor)))
    profile.append(list(main.SQL_Profile_Search('Github_Link', (0,), cursor)))
    profile.append(list(main.SQL_Profile_Search('Projects', (0,), cursor)))
    profile.append(list(main.SQL_Profile_Search('Classes', (0,), cursor)))
    profile.append(list(main.SQL_Profile_Search('Personal_Info', (0,), cursor)))
    profile.append(list(main.SQL_Profile_Search('Email', (0,), cursor)))
    profile.append(list(main.SQL_Profile_Search('Phone_Number', (0,), cursor)))
    new_profile = main.Fix_SQL_Return_Strings(profile)

    cover_letter, resume = main.Query_LLM(new_job, new_profile, model)

    # Check strings containing profile/job info is contained in generated cover letter/resume
    isContained = True
    for i in range(3):
        if ((str(new_profile[i]).lower() in (str(cover_letter)).lower()) or
                (str(new_profile[i]).lower() in (str(resume)).lower())):
            pass
        else:
            isContained = False
            break

    if (str(new_job[0]).lower() in (str(cover_letter)).lower()) or (str(new_job[0]).lower() in (str(resume)).lower()):
        pass
    else:
        isContained = False

    assert isContained == True


def test_check_empty_string():
    test = ['', '', '', '']
    assert main.check_empty_string(test) is True

    test = ['aaaa', 'aaaa', 'aaaa', 'aaaa']
    assert main.check_empty_string(test) is False

    test = ['aaaa', 'aaaa', 'aaaa', '']
    assert main.check_empty_string(test) is True

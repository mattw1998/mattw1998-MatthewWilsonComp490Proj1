import json
import sqlite3


# Reads json files with one object per line into a list
def single_json_to_list(file_path):
    json_obj2 = []
    try:
        with open(file_path) as file:
            for line in file:
                json_obj2.append(json.loads(line))
    except FileNotFoundError:
        print("file", file_path, "was not found")
    return json_obj2


# Reads json files with multiple objects per line into a list
def multi_json_to_list(file_path):
    json_obj = []
    try:
        with open("rapid_jobs2.json") as file:
            for line in file:
                data = json.loads(line)
                for i in data:
                    json_obj.append(i)
    except FileNotFoundError:
        print("file", file_path, "was not found")
    return json_obj


def create_table():
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS jobs (
            id varchar(50) primary key,
            title varchar(50),
            company varchar(50),
            description varchar(2000),
            image_url varchar(50),
            location varchar(50),
            employment_type varchar(30),
            date_posted varchar(50),
            salary_range varchar(50),
            job_providers varchar(2000),
            site varchar(50),
            job_url varchar(100),
            job_url_direct varchar(100),
            salary_source varchar(40),
            interval varchar(40),
            min_amount real,
            max_amount real,
            currency varchar(30),
            is_remote varchar(30),
            job_level varchar(30),
            job_function varchar(40),
            company_industry varchar(40),
            listing_type varchar(50),
            emails varchar(100),
            company_url varchar(50),
            company_url_direct varchar(50),
            company_addresses varchar(50),
            company_num_employees varchar(30),
            company_revenue varchar(30),
            company_description varchar(2000),
            ceo_name varchar(40)
        )
    """
    )


# inserts the list that contains the json with mult. objects per line into the sql database
def insert_multi_json_to_sql(json_obj_list):
    insert_statement = (
        "INSERT INTO jobs (id, title, company, description, image_url, location, employment_type,"
        " date_posted, salary_range, job_providers) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    )
    for i in json_obj_list:
        try:
            job_dict = dict(i)
            insert_data = (
                job_dict.get("id"),
                job_dict.get("title"),
                job_dict.get("company"),
                job_dict.get("description"),
                job_dict.get("image"),
                job_dict.get("location"),
                job_dict.get("employment_type"),
                job_dict.get("date_posted"),
                job_dict.get("salary_range"),
                job_dict.get("job_providers"),
            )
            cursor.execute(insert_statement, insert_data)
            job_dict.clear()
        except sqlite3.IntegrityError:
            print("Entry", i, "already exists in table")


# inserts the list that contains the json with one object per line into the sql database
def insert_single_json_to_sql(json_obj_list):
    insert_statement = (
        "INSERT INTO jobs (id, site, job_url, job_url_direct, title, company, location,"
        " employment_type, date_posted, salary_source, interval, min_amount, max_amount,"
        " currency, is_remote, job_level, job_function, company_industry, listing_type, emails,"
        " description, company_url, company_url_direct, company_addresses, company_num_employees,"
        " company_revenue, company_description, image_url, ceo_name)"
        " VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    )
    for i in json_obj_list:
        try:
            job_dict = dict(i)
            insert_data = (
                job_dict.get("id"),
                job_dict.get("site"),
                job_dict.get("job_url"),
                job_dict.get("job_url_direct"),
                job_dict.get("title"),
                job_dict.get("company"),
                job_dict.get("location"),
                job_dict.get("job_type"),
                job_dict.get("date_posted"),
                job_dict.get("salary_source"),
                job_dict.get("interval"),
                job_dict.get("min_amount"),
                job_dict.get("max_amount"),
                job_dict.get("currency"),
                job_dict.get("is_remote"),
                job_dict.get("job_level"),
                job_dict.get("job_function"),
                job_dict.get("company_industry"),
                job_dict.get("listing_type"),
                job_dict.get("emails"),
                job_dict.get("description"),
                job_dict.get("company_url"),
                job_dict.get("company_url_direct"),
                job_dict.get("company_addresses"),
                job_dict.get("company_num_employees"),
                job_dict.get("company_revenue"),
                job_dict.get("company_description"),
                job_dict.get("logo_photo_url"),
                job_dict.get("ceo_name"),
            )
            cursor.execute(insert_statement, insert_data)
            job_dict.clear()
        except sqlite3.IntegrityError:
            print("Entry", i, "already exists in table")


def save_database():
    connection.commit()
    connection.close()


if __name__ == "__main__":
    json_obj = []
    json_obj2 = []
    json_obj2 = multi_json_to_list("rapid_jobs2.json")
    json_obj = single_json_to_list("rapidResults.json")
    connection = sqlite3.connect("job_ads.db")
    cursor = connection.cursor()
    create_table()
    insert_multi_json_to_sql(json_obj)
    insert_single_json_to_sql(json_obj2)
    save_database()

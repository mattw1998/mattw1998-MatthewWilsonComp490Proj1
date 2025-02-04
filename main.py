import google.generativeai as genai

if __name__ == '__main__':

    # configure gemini AI w/ api key
    genai.configure(api_key="AIzaSyCexoSxIJ372OV-j-h6Ln-fWg8mQUIjhoA")
    model = genai.GenerativeModel("gemini-1.5-flash")

    job_title = input("Enter the title of a job posting: ")
    job_description = input("Enter a description for the job entered: ")
    personal_description = input("Enter a description of yourself, including relevant skills: ")

    # send query to AI model and store response
    query = ("Given the job, ", job_title, "with a description ", job_description, ". ",
    "Give me a sample resume in markdown format, for someone with these skills. ",
    personal_description)
    response = model.generate_content(query)
    print('Query 1 result: \n')
    print(response.text)

    query = ("Given the job, ", job_title, "with a description ", job_description, ". ",
             "Give me a sample resume in markdown format. Relevant personal skills to be included are, ", personal_description)
    response = model.generate_content(query)
    print('\n\n\nQuery 2 result: \n')
    print(response.text)

    query = ("Based on these skills, ", personal_description,
             ". Create a resume in markdown format for the job, ", job_title,
             ", with a description of ", job_description)
    response = model.generate_content(query)
    print('\n\n\nQuery 3 result: \n')
    print(response.text)


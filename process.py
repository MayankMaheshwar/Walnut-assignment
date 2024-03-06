
"learnings"








# # from langchain_openai import OpenAI
# # import re
# #

# from dotenv import load_dotenv
# import google.generativeai as genai
# import os
# import re


# load_dotenv()
# ## load all the environemnt variables


# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


#  # input_db = SQLDatabase.from_uri('sqlite:///users.db')
#     # llm_1 = OpenAI(temperature=0,api_key="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")

#     # db_agent = SQLDatabaseChain(llm = llm_1,
#     #                             database = input_db,
#     #                             verbose=True)

# import sqlite3

# def run_sql_query(database_path, sql_query):
#     """
#     Executes an SQL query and returns the results.

#     :param database_path: Path to the SQLite database file.
#     :param sql_query: The SQL query to be executed.
#     :return: The result of the SQL query.
#     """
#     # Connect to the SQLite database
#     conn = sqlite3.connect(database_path)
#     cursor = conn.cursor()

#     try:
#         # Execute the SQL query
#         cursor.execute(sql_query)

#         # If the query was a SELECT, fetch and return the results
#         if sql_query.strip().upper().startswith('SELECT'):
#             results = cursor.fetchall()
#         else:
#             # If the query modified data, commit the changes and return the number of affected rows
#             conn.commit()
#             results = cursor.rowcount

#     except sqlite3.Error as e:
#         print(f"An error occurred while executing the SQL query: {e}")
#         results = None

#     finally:
#         # Close the database connection
#         cursor.close()
#         conn.close()

#     return results


# def process_text(question, user_id):
#     print("pass")
#     ans = ""
#     response = ""
#     try:
#         if 'me' in question or 'my' in question:
#             user_id_str = str(user_id)
#             question = re.sub(r'\bme\b|\bmy\b', user_id_str, question)
#         print(question,"ct")

#         prompt =[
#                 """
#                 You are an expert in converting English questions to SQL query!
#                 The SQL database have three tables - \n
#                 1) User - (id, fullname, username, password, user_type (patient or doctor)) \n, 
#                 2) Availability(id, doctor_id, day, start_time, end_time) \n, 
#                 3) Appointment (id, doctor_id, patient_id, appoitment_date, start_time and end_time). \n
#                 For example,\nExample 1 - How many patients user are present? \n, 
#                 the SQL command will be something like this SELECT COUNT(*) FROM User where user_type = "patient" \n;
#                 \nExample 2 - Tell me name of all doctors who are available between start_time to end_time? \n, 
#                 the SQL command will be something like this SELECT fullname FROM User 
#                 inner join Availability on User.id=Availability.doctor_id where user_type = "doctor" and given_start_time>=Availability.start_time and given_end_time<=Availability.end_time \n; 
#                 Also the sql code should not have ``` in beginning or end and sql word in output
#                 """
            
#             ]

#         model = genai.GenerativeModel('gemini-pro')
#         sub_ans = model.generate_content([prompt[0], question]).text

#         # question = database_info + question
#         # ans = db_agent.run(question)
#         print(sub_ans,"ans")

#         ans = run_sql_query("users.db", sub_ans)
#         print(ans,"ans")
#         if "schedule" in question.lower():
#             response = "schedule response is "+ans

#         elif "cancel" in question.lower():
            
#             response = "cancel response is "+ans

#         elif "reschedule" in question.lower():
            
#             response = "reschedule response is "+ans
#         else:
#             response = "Hi, Currently I can only cancel, schedule or reschedule your appoitments with doctors"

#         return response
#     except Exception as e:
#         response = "some exception occured"
#         print(e,"exceptn")
#     finally:
#         return response
        



"learnings"

# from openai import OpenAI
# from dotenv import load_dotenv
# import os
# import re

# load_dotenv()

# client = OpenAI(api_key=os.getenv("OPENAI_SECRET_KEY"))


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
#             user_id_str = "patient_user_id =" + str(user_id)
#             question = re.sub(r'\bme\b|\bmy\b', user_id_str, question)
#         print(question,"ct")

#         response = client.chat.completions.create(
#         model="gpt-4-0125-preview",
#         messages=[
#             {"role": "system", "content": """
#                         You are an expert in converting English questions to SQL query!
#                         The SQL database have three tables - \n
#                         1) User - (id, fullname, username, password, user_type (patient or doctor)) \n, 
#                         2) Availability(id, doctor_id, day, start_time, end_time) \n, 
#                         3) Appointment (id, doctor_id, patient_id, appoitment_date, start_time and end_time). \n
#                         For example,\nExample 1 - How many patients user are present? \n, 
#                         the SQL command will be something like this SELECT COUNT(*) FROM User where user_type = "patient" \n;
#                         \nExample 2 - Tell me name of all doctors who are available between start_time to end_time? \n, 
#                         the SQL command will be something like this SELECT fullname FROM User 
#                         inner join Availability on User.id=Availability.doctor_id where user_type = "doctor" and given_start_time>=Availability.start_time and given_end_time<=Availability.end_time \n; 
#                         Just give the sql query code in string format and make sure it should not have ``` in beginning or end and sql word in output
#                         """},

#             {"role": "user", "content": f"{question}"},
            
#         ]
#         )
#         print(response)
#         sub_ans = response.choices[0].message.content

#         print(sub_ans,"ans")

#         ans = run_sql_query("users.db", sub_ans)
#         print(ans,type(ans),"ans")
#         # Process the extracted text command
#         if "schedule" in question.lower():
#             # Extract details and call schedule_appointment
#             response = "schedule response is "+ str(ans)

#         elif "cancel" in question.lower():
#             # Extract appointment ID and call cancel_appointment
            
#             response = "cancel response is "+ans

#         elif "reschedule" in question.lower():
#             # Extract details and call reschedule_appointment
            
#             response = "reschedule response is "+ans
#         else:
#             response = "Hi, Currently I can only cancel, schedule or reschedule your appoitments with doctors"

#         return response
#     except Exception as e:
#         response = "some exception occured"
#         print(e,"exceptn")
#     finally:
#         return response
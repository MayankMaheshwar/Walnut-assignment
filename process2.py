import os
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import *
from langchain_community.utilities.sql_database import SQLDatabase
from dotenv import load_dotenv
import re

load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPENAI_SECRET_KEY"), model_name="gpt-4-0125-preview")

db_uri = "sqlite:///instance/users.db"
input_db = SQLDatabase.from_uri(db_uri)

toolkit = SQLDatabaseToolkit(db=input_db,llm=llm)

# Create an agent executor
agent_executor = create_sql_agent(
    llm=llm,
    handle_parsing_errors=True,
    toolkit=toolkit,
    verbose=True
)

def process_text(question, user_id):
    result = ""
    try:
        if 'me' in question or 'my' in question:
            user_id_str = "patient_user_id -" + str(user_id)
            question = re.sub(r'\bme\b|\bmy\b', user_id_str, question)

        question = question + ". If book or schedule words is in the question, make sure to delete the record from availability for that particular doctor after successfully adding the record in appoitment."
        # Execute the command
        result = agent_executor.run(question)
        print(result,"result")

    except Exception as e:
        result = "something went wrong please try again"
        print(e,"exception")
    finally:
        return result
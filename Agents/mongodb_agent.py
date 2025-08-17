from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os

from custom_tools.mongodb import insert_data
from autogen_core.tools import FunctionTool

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

insert_data_tool = FunctionTool(insert_data,description='insert parsed resume data to mongodb collection',
                                name='insert_data')

model_client = OpenAIChatCompletionClient(
    model='gpt-4o-mini',
    api_key=api_key,
)

SYSTEM_MESSAGE = """
Your are a database agent. your task is to add data parsed data from resume_parser_agent.'
Always use 'insert_data' tool to add json data to database
"""

def get_mongodb_agent():
    """
    Returns an instance of the AssistantAgent configured for resume parsing.
    """
    mongodb_agent = AssistantAgent(name='mongodb_agent',
                                         model_client=model_client,
                                         system_message=SYSTEM_MESSAGE,
                                         tools=[insert_data_tool])
    return mongodb_agent  

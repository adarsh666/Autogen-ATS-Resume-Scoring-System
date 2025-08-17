from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os

from schema.user_details import UserDetails

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

structured_model_client = OpenAIChatCompletionClient(
    model='gpt-4o-mini',
    temperature=0.0,
    top_p=1,
    seed=42,
    max_tokens=500,
    api_key=api_key,
    response_format=UserDetails
)

def get_resume_parser_agent():
    """
    Returns an instance of the AssistantAgent configured for resume parsing.
    """
    resume_parser_agent = AssistantAgent(name='resume_parser_agent',model_client=structured_model_client)
    return resume_parser_agent

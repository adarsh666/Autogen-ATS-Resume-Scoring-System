from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os

from schema.ats_details import ResumeScore
from prompts.agent_prompt import ats_agent_prompt

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

structured_model_client = OpenAIChatCompletionClient(
    model='gpt-4o-mini',
    api_key=api_key,
    response_format=ResumeScore
)

def get_ATS_scoring_agent():
    """
    Returns an instance of the AssistantAgent configured for ATS Scoring.
    """
    resume_parser_agent = AssistantAgent(name = 'ats_scoring_agent',
                                         model_client = structured_model_client,
                                         system_message = ats_agent_prompt)
    return resume_parser_agent

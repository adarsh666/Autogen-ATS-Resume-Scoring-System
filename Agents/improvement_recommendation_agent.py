from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os

from custom_tools.vector_db import jd_search
from prompts.agent_prompt import improvement_recommendation_agent_prompt
from autogen_core.tools import FunctionTool


load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

model_client = OpenAIChatCompletionClient(
    model='gpt-4o-mini',
    api_key=api_key,
)

retrival_tool = FunctionTool(jd_search,description='A tool to extract job descriptions from vector db')

def get_improvement_recommendation_agent():
    """
    Returns an instance of the AssistantAgent configured for resume improvement recommendation.
    """
    recommendation_agent = AssistantAgent(name='improvement_recommendation_agent',
                                       model_client=model_client,
                                       system_message=improvement_recommendation_agent_prompt,
                                       reflect_on_tool_use=True)
    return recommendation_agent

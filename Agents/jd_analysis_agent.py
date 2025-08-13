from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os

from custom_tools.tools import jd_search
from prompts.agent_prompt import jd_analysis_agent_prompt
from autogen_core.tools import FunctionTool


load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

model_client = OpenAIChatCompletionClient(
    model='gpt-4o',
    api_key=api_key,
)

retrival_tool = FunctionTool(jd_search,description='A tool to reverse a string')

def get_jd_analysis_agent():
    """
    Returns an instance of the AssistantAgent configured for job description analysis.
    """
    jd_analysis_agent = AssistantAgent(name='job_description_analysis_agent',
                                       model_client=model_client,
                                       system_message=jd_analysis_agent_prompt,
                                       tools=[retrival_tool])
    return jd_analysis_agent

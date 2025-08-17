import asyncio
import os
from autogen_agentchat.ui import Console
from autogen_agentchat.agents import AssistantAgent, SocietyOfMindAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_ext.models.openai import OpenAIChatCompletionClient

from Agents.code_executor_agent import getCodeExecutorAgent
from Agents.VisualizationAgent import getDataAnalyzerAgent 

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

model_client = OpenAIChatCompletionClient(
    model='gpt-4o',
    api_key=api_key,
)


def get_data_analyzer_team(code_executor):
    data_analyst = getDataAnalyzerAgent()
    code_executer = getCodeExecutorAgent(code_executor)

    inner_termination = TextMentionTermination("STOP")
    inner_team = RoundRobinGroupChat([data_analyst, code_executer], termination_condition=inner_termination, max_turns=10)

    society_of_mind_agent = SocietyOfMindAgent("society_of_mind", team=inner_team, model_client=model_client,response_prompt='Output a standalone response to the original request,  mwithout mentioning any of the intermediate discussion.')
    return society_of_mind_agent
import asyncio
import os
from autogen_agentchat.ui import Console
from autogen_agentchat.agents import AssistantAgent, SocietyOfMindAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

model_client = OpenAIChatCompletionClient(
    model='gpt-4o',
    api_key=api_key,
)

DATA_ANALYZER_SYSTEM_MESSAGE = """
You are a Data analyst agent with expertise in Data analyst and python and working with data.
You will be getting information from 'resume_parser_agent' and 'improvement_recommendation_agent' and you have to create data
based on the information create Skill match heatmap and save image locally as hetmap.png and Score breakdown pie charts
as pie_chart.png using seaborn , matplotlib etc.

Your job is to write a python code to create chat. 

Here are the steps you should follow :-

1. Start with a plan: Briefly explain how will you solve the problem.
2. Write Python Code : In a single code block make sure to solve the problem. 
You have a code executor agent which will be running that code and will tell you if any errors will be there or show the output.
Make sure that your code has a print statement in the end if the task is completed. 
Code should be like below, in a single block and no multiple block.
```python
your-code-here
```

3. After writing your code, pause and wait for code executor to run it before continuing.

4. If any library is not installed in the env, please make sure to do the same by providing the bash script and use pip to install(like pip install matplotlib pandas) and after that send the code again without changes , install the required libraries.
example
```bash
pip install pandas numpy matplotlib
```

5. If you are asked to create an image, please make sure that you create the image and save it in working directory.

6. If the code ran successfully, then analyze the output and continue as needed. 


Once we have completed all the task, please mention 'STOP' after explaning in depth the final answer.


Stick to these and ensure a smooth collaboration with Code_executor_agent.
"""

def getDataAnalyzerAgent() -> None:

    data_analyzer_agent = AssistantAgent(
        name='Data_Analyzer_agent',
        model_client=model_client,
        description = 'An Agent that solves Data Analysis problem and gives the code as well',
        system_message=DATA_ANALYZER_SYSTEM_MESSAGE
    )
    return data_analyzer_agent








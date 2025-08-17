
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from Agents import improvement_recommendation_agent
from Agents.parser_agent import get_resume_parser_agent
from Agents.ats_scoring_agent import get_ATS_scoring_agent
from Agents.jd_analysis_agent import get_jd_analysis_agent
from Agents.improvement_recommendation_agent import get_improvement_recommendation_agent
from Agents.code_executor_agent import getCodeExecutorAgent
from Agents.VisualizationAgent import getDataAnalyzerAgent
from Agents.SocietyOfMindsAgent import get_data_analyzer_team
from Agents.mongodb_agent import get_mongodb_agent


def getDataAnalyzerTeam(docker):

    resume_parser_agent = get_resume_parser_agent()

    mongodb_agent = get_mongodb_agent()

    ats_scoring_agent = get_ATS_scoring_agent()

    jd_analyser_agent = get_jd_analysis_agent()

    improvement_recommendation_agent = get_improvement_recommendation_agent()

    code_executor_agent = get_data_analyzer_team(docker)


    text_mention_termination = TextMentionTermination('STOP')

    team = RoundRobinGroupChat(
        participants=[resume_parser_agent, mongodb_agent, ats_scoring_agent,
                      jd_analyser_agent, improvement_recommendation_agent, code_executor_agent],
        max_turns=6,
        termination_condition=text_mention_termination
    )

    return team
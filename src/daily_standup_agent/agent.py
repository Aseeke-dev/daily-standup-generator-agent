import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnableParallel, RunnableLambda
from .schema import StandUpUpdate
from .prompts import prompt
from .tools.calender_tool import fetch_calendar_events
from .tools.jira_tool import fetch_jira_tickets
from .tools.slack_tool import post_to_slack

load_dotenv()
    
def generate_standup():
    
    parallel_fetcher = RunnableParallel(
        calendar = RunnableLambda(lambda x: fetch_calendar_events()),
        tasks = RunnableLambda(lambda x: fetch_jira_tickets())
    )
    
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")
    structured_llm = llm.with_structured_output(StandUpUpdate)
    
    chain = parallel_fetcher | prompt | structured_llm
    
    result = chain.invoke({})
    
    formatted_standup = f"*Yesterday I...*\n{result.yesterday}\n\n*Today I...*\n{result.today}\n\n*Blockers:*\n{result.blockers}"
    
    print("\n==============================")
    print("📢 LIVE GENERATED STAND-UP")
    print("==============================")
    print(formatted_standup)
    print("==============================")
    
    print("Posting up update to slack...")
    slack_response = post_to_slack(formatted_standup)
    print(slack_response)


if __name__ == "__main__":
    generate_standup()
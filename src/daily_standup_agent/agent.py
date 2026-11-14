import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from .schema import StandUpUpdate
from .mock_calender import YESTERDAY_MEETINGS, TODAY_MEETINGS

load_dotenv()

def read_task():
    with open("tasks.txt", "r") as file:
        return file.read()
    
def generate_standup():
    print("🚀 Starting Phase 1 Sandbox Test...\n")
    
    tasks_data = read_task()
    calender_data = f"Yesterday's Meetings: {YESTERDAY_MEETINGS}\n Today's Meetings: {TODAY_MEETINGS}\n"
    
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")
    
    structured_llm = llm.with_structured_output(StandUpUpdate)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a strict assistant generating a daily stand-up update. 
        Extract completed tasks and yesterday's meetings for the 'yesterday' field. 
        Extract 'In Progress' tasks and today's meetings for the 'today' field. 
        Identify any blockers for the 'blockers' field. 
        Format all fields as clean, professional bullet points."""),
        ("human", "Tasks Data:\n{tasks}\n\nCalendar Data:\n{calendar}")
    ])
    
    chain = prompt | structured_llm
    
    result = chain.invoke({
        "tasks": tasks_data,
        "calendar": calender_data
    })
    
    print("--- Generated Result ---")
    print(f"**Yesterday, I..**\n{result.yesterday}\n")
    print(f"**Today, I...**\n{result.today}\n")
    print(f"**Blockers:**\n{result.blockers}\n")


if __name__ == "__main__":
    generate_standup()
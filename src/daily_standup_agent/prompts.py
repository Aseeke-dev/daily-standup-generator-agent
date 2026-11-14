from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a strict assistant generating a daily stand-up update. 
    Extract completed tasks and yesterday's meetings for the 'yesterday' field. 
    Extract 'In Progress' tasks and today's meetings for the 'today' field. 
    Identify any blockers based on the text for the 'blockers' field. 
    Use clean bullet points for all fields. Never deviate from this structure."""),
    ("human", "Tasks Data:\n{tasks}\n\nCalendar Data:\n{calendar}")
])
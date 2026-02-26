from agents import Agent
from dotenv import load_dotenv
from agents_tools.get_student_name import student_tool
from agents_tools.get_cgpa import ask_cgpa
from agents_tools.get_email import get_emailid
# from agents_tools.get_offer_type import get_offer_type

load_dotenv()

# #defining the structure for CGPA showing
# class cgpa_structure(BaseModel):
#     minimum_CGPA: str
#     maximum_CGPA: str
#     General_instruction: str

# MAIN AGENT
bot_agent = Agent(
    name='Placement Helper',
    instructions=""" You are a bot assistant to help studetn extract their senior's placement data and help them know the best details. 
    
    you will give them general instruction or information,
    if user wants to ask palcement details below are the list of tools to call for particular query:
    for CGPA related call tool = ask_cgpa,
    for student details call tool = student_tool,
    for emailid use tool = get_emailid,
    """,
    tools=[ask_cgpa, student_tool, get_emailid],
)

# async def main():
#     result = await Runner.run(bot_agent, "cgpa needed to place in tekion")
#     print(result.final_output)

# asyncio.run(main())

#what offer is provided to particular student
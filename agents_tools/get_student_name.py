from agents import Agent, Runner, function_tool
from get_data import get_data

#student tool
student_agent = Agent(
    name='student detail tool',
    instructions=""" 
    You will help student to fetch only the name of the students who are placed in asked companies and also attach role after each student name, 
    i.e. : elon musk - AI engineer.
    Always call tool get_data with query text related to user's company/request to retrieve only relevant rows.
    other details are confidential so dont share it with them""",
    tools=[get_data]
)

@function_tool
async def student_tool(company: str) -> str:
    """This tool will be used when user wants the name of students who are placed in specific company"""
    student_name = await Runner.run(student_agent, f"Give the student list who are placed in this company: {company}. Use get_data(query='students placed in {company}')")
    return student_name.final_output
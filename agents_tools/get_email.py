from agents import Agent, Runner, function_tool
from get_data import get_data

email_agent = Agent(
    name="email provider",
    instructions="""
    you are a helper to give student id now you will have a data of student you will have to find that student's student-id mentioned in the data after getting id of the student you will have to return response in below format:
    '<id>@dau.ac.in' i.e. if student id is 202209999 return 202209999@dau.ac.in
    Always call tool get_data with query text containing student name before final answer.
    """,
    tools=[get_data]
)

@function_tool
async def get_emailid(student_name: str) -> str:
    email = await Runner.run(email_agent, f"get the email id for {student_name}. Use get_data(query='student id for {student_name}')")
    return email.final_output
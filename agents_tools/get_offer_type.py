from agents import Agent, Runner, function_tool
from get_data import get_data

offer_agent = Agent(
    name='Offer type provider',
    instructions="""
    your task is to provide offer type of the student whatever query user asks
    in the data I means internship only, job will be performance based
    J means Job only
    and I+J means internship + job

    if usered asked for any company then provide general offer provided at company if ask for particular student you have offer type of student in data then show it that then
    """,
    tools=[get_data]
)

@function_tool
async def get_offer_type():
    result = await Runner.run(offer_agent, 'fullfil the user query requirement')
    return result.final_output
from agents import Agent, Runner, function_tool, InputGuardrailTripwireTriggered
from get_data import get_data
from guardrails.input import cpga_prohibited

#CGPA tool
cgpa_agent = Agent(
    name='CGPA Provider',
    instructions=""" 
    whenever user ask about cgpa from the data, provide minimum CGPA and maximum CGPA no need to provide every student CGPA and also keep in mind you will not provide any student's particular CGPA
    print like this:
    minimum CGPA - extract the minimum cgpa from that company same for maximum
    this is just to provide student range so that they can prepre accordingly
    Always call tool get_data with a focused query before answering.
    """,
    tools=[get_data],
    input_guardrails=[cpga_prohibited]
    # output_type=cgpa_structure
)

@function_tool
async def ask_cgpa(company: str)-> str:
    """ this tool will help user any query related to cgpa or cpi """
    try:
        cgpa = await Runner.run(cgpa_agent, f"fullfil detials for user for the {company}. Use get_data(query='cgpa cpi range for {company}')")
        return cgpa.final_output
    except InputGuardrailTripwireTriggered as e:
        print('Trip wire Triggered')
        return str(e)
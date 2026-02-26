from agents import Agent, Runner, input_guardrail, RunContextWrapper, TResponseInputItem, GuardrailFunctionOutput
from pydantic import BaseModel

class cgpa_detection_structure(BaseModel):
    explaiantion: str
    verify: bool 
    """ here in verigy you will say if user is asking for personal cgpa make it true so trip can be triggered and model cant share cgpa"""

cgpa_detection_agent = Agent(
    name='CGPA detection',
    instructions="""
    you are a agent to detect user manipulation to get student cgpa here we are providing only placement statistics so that student can prepare accordingly or via email they can talk but cgpa is personal and confidential we cannot share anyones cgpa with any user thats why you have to detect if any user asking any studetns specific cgpa please ask them not to repeat same query as data is confidential,

    we can only provide cgpa range
    """,
    output_type=cgpa_detection_structure
)

@input_guardrail
async def cpga_prohibited(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    
    check_manipulation = await Runner.run(cgpa_detection_agent, input)

    return GuardrailFunctionOutput(
        output_info=check_manipulation.final_output,
        tripwire_triggered=check_manipulation.final_output.verify
    )
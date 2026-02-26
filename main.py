from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from agents import Runner, SQLiteSession
from bot_main import bot_agent

app = FastAPI()

session = SQLiteSession('convo123', 'history_chat.db')

class QueryRequest(BaseModel):
    query: str


def _extract_token_usage(result: object) -> tuple[int | None, int | None, int | None]:
    usage = getattr(result, "usage", None)
    if usage is None and isinstance(result, dict):
        usage = result.get("usage")

    if usage is None:
        return None, None, None

    if isinstance(usage, dict):
        input_tokens = usage.get("input_tokens")
        output_tokens = usage.get("output_tokens")
        total_tokens = usage.get("total_tokens")
    else:
        input_tokens = getattr(usage, "input_tokens", None)
        output_tokens = getattr(usage, "output_tokens", None)
        total_tokens = getattr(usage, "total_tokens", None)

    return input_tokens, output_tokens, total_tokens

@app.post("/placementbot")
async def ask_bot(data: QueryRequest):
    result = await Runner.run(bot_agent, data.query, session=session)
    input_tokens, output_tokens, total_tokens = _extract_token_usage(result)

    if input_tokens is not None or output_tokens is not None or total_tokens is not None:
        print(
            "Token usage -> "
            f"input: {input_tokens if input_tokens is not None else 'N/A'}, "
            f"output: {output_tokens if output_tokens is not None else 'N/A'}, "
            f"total: {total_tokens if total_tokens is not None else 'N/A'}"
        )
    else:
        print("Token usage not available on runner result.")

    # print(result.final_output)
    return JSONResponse(status_code=200, content={'Bot response': result.final_output})

@app.post('/clear_chat')
async def clear_data():
    await session.clear_session()
    return JSONResponse(status_code=200, content={'status': 'Chat cleared'})
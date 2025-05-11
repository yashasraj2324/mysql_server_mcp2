from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai_agent.agent import natural_to_sql, call_mcp_tool

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryPrompt(BaseModel):
    prompt: str

@app.post("/query")
async def handle_query(body: QueryPrompt):
    sql = natural_to_sql(body.prompt)
    result = call_mcp_tool(sql)
    return {"sql": sql, "result": result}

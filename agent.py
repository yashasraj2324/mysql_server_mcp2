import os
from transformers import pipeline
import subprocess
import json
import mysql.connector
from ai_agent.prompt_templates import to_sql_prompt

llm = pipeline("text2text-generation", model="google/flan-t5-base")

def get_all_table_names():
    conn = mysql.connector.connect(
        host="localhost",
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "advaith")
    )
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

def natural_to_sql(prompt: str) -> str:
    tables = get_all_table_names()
    template = to_sql_prompt(prompt, tables)
    result = llm(template, max_length=128, do_sample=False)[0]["generated_text"]
    return result.strip()

def call_mcp_tool(sql: str):
    payload = {
        "type": "tool_call",
        "toolName": "execute_sql",
        "args": {"query": sql}
    }

    proc = subprocess.Popen(
        ["python", "mcp_server/mysql_mcp_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = proc.communicate(input=json.dumps(payload) + "\n")
    return stdout or stderr

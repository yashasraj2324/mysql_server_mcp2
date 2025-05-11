def to_sql_prompt(user_prompt: str, tables: list[str]):
    table_list = ", ".join(tables)
    return f"""
    You are a helpful assistant. These are the available MySQL tables: {table_list}.
Based on the user's instruction, write an SQL query using the appropriate table.
Instruction: {user_prompt}
SQL:
"""
    

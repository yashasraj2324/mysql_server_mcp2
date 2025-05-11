from ai_agent.agent import natural_to_sql, call_mcp_tool

if __name__ == "__main__":
    user_input = input("Ask a question: ")
    sql = natural_to_sql(user_input)
    print(f"\nGenerated SQL:\n{sql}\n")
    print("Sending to MCP server...")
    result = call_mcp_tool(sql)
    print("\nResult:\n", result)

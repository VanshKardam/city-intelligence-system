import sys
import os
sys.path.append(r"c:\Users\hp\Desktop\city intelligence system")
from Agent import agent

try:
    print("Invoking agent...")
    result = agent.invoke({"messages": [("user", "What is the weather in Ghaziabad?")]})
    print("KEYS:", result.keys())
    print("MESSAGES:")
    for msg in result["messages"]:
        print(type(msg), getattr(msg, "content", ""), getattr(msg, "tool_calls", []))
except Exception as e:
    print("ERROR:", e)

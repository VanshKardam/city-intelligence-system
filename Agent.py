# First step - loading all the libraries
from dotenv import load_dotenv
load_dotenv()
import os
import requests
from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from tavily import TavilyClient
from rich import print

# Now lets create some tools

# Weather tool
@tool
def get_weather(city : str) -> str:
    """
    Get current weather of a city
    """
    # Placing the API key directly here for now so it works
    API_KEY = "e403f63625c1cae39a5ad72540213c9c"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    print("DEBUG:", data)

    if str(data.get("cod")) != "200":
        return f"Error: {data.get('message', 'Unknown error')}"
    
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    return f"Weather in {city}: {desc}, {temp} degrees Celcius."

# print(get_weather.invoke("Ghaziabad"))

# Tavily news tool

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def get_news(city: str) -> str:
    """
    Get Latest news about the city
    """
    response = tavily_client.search(
        query = f"latest news in {city}",
        search_depth = "basic",
        max_results = 3
    )
    results = response.get("results", [])
    if not results:
        return f"No news found for {city}"
    news_list = []
    for r in results:
        title = r.get("title", "No title")
        url = r.get("url", "")
        snippet = r.get("content", "")

        news_list.append(
            f"-{title}\n{url}\n{snippet[:100]}..."
        )
    
    return f"Latest news in {city} : \n {'\n'.join(news_list)}"


# print(get_news.invoke("Ghaziabad"))

llm = ChatMistralAI(model="mistral-medium-latest")

tools = ({
    "get_weather" : get_weather,
    "get_news" : get_news
})

llm_with_tool = llm.bind_tools([get_news, get_weather])

if __name__ == "__main__":
    #Agent LOOP - very important
    messages = []
    
    print("City Intelligence System")
    print("Enter 0 to quit")
    print("---------------------------------------")
    
    while True:
        user_input = input("You : ")
        if user_input == "0":
            print("Exiting the AI system. Thanks for using!")
            break
        messages.append(HumanMessage(content = user_input))
    
        while True:
            result = llm_with_tool.invoke(messages)
            messages.append(result)
    
            # if tool is required
            if result.tool_calls:
                for tool_call in result.tool_calls:
                    tool_name = tool_call["name"]
    
                    # human in the loop
                    confirm = input(f"Do you want to allow the tool {tool_name} to run? (y/n) : ")
                    if confirm.lower() != "y":
                        print("Exiting")
                        break
                    else:
                        tool_result = tools[tool_name].invoke(tool_call)
                        messages.append(
                            ToolMessage(
                                content = tool_result,
                                tool_call_id = tool_call["id"])
                        )
                continue
            else:
                print("AI : ", result.content)
                messages.append(result)
                break
        
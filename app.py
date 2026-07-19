import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
# Import our LLM and tools from Agent.py
from Agent import llm_with_tool, tools

st.set_page_config(page_title="City Intelligence Agent", page_icon="🏙️")
st.title("🏙️ City Intelligence System")
st.markdown("Ask me about the **weather** or **latest news** in any city!")

# Initialize chat history in Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages from history on app rerun
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage) and message.content:
        # Only print AIMessages if they have text content (ignore tool call requests)
        with st.chat_message("assistant"):
            st.markdown(message.content)
    elif isinstance(message, ToolMessage):
        with st.chat_message("assistant", avatar="🛠️"):
            with st.expander("Tool Output"):
                st.markdown(message.content)

# React to user input
if prompt := st.chat_input("What would you like to know?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append(HumanMessage(content=prompt))

    with st.spinner("Thinking..."):
        # The Agent Loop
        while True:
            # Get response from LLM
            result = llm_with_tool.invoke(st.session_state.messages)
            st.session_state.messages.append(result)

            # If the LLM decided to use a tool
            if result.tool_calls:
                for tool_call in result.tool_calls:
                    tool_name = tool_call["name"]
                    
                    with st.chat_message("assistant", avatar="⚙️"):
                        st.markdown(f"*Running {tool_name}...*")
                    
                    # Execute tool automatically
                    tool_result = tools[tool_name].invoke(tool_call)
                    
                    # Append result to history
                    tool_msg = ToolMessage(content=tool_result, tool_call_id=tool_call["id"])
                    st.session_state.messages.append(tool_msg)
                    
                    # Display tool result hidden in an expander for clean UI
                    with st.chat_message("assistant", avatar="🛠️"):
                        with st.expander("Tool Output"):
                            st.markdown(tool_result)
                
                # Continue the loop so the LLM can read the tool output and generate a final answer
                continue
            
            else:
                # No tools requested, the LLM gave a final answer
                with st.chat_message("assistant"):
                    st.markdown(result.content)
                # Break the loop, waiting for next user input
                break

import functools
import operator
import os

from langchain_openai import ChatOpenAI
from SYSTEM_PROMPTS import SCRIPT_GENERATOR_PROMPT
from main import set_environment_variables
from typing import Annotated, Sequence, TypedDict
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import END, StateGraph
from langchain_community.tools.tavily_search import TavilySearchResults
import asyncio
import operator
import uuid
from colorama import Fore, Style
from tools import calculator, dox_fool, generate_image, research
import streamlit as st
from typing import Annotated, Literal, TypedDict
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
set_environment_variables("WHaK AI")
#LLM = ChatOpenAI(model="gpt-3.5-turbo-0125")

SCRIPT_AGENT_NAME = "script_agent"
TAVILY_TOOL = TavilySearchResults(max_results=10, tavily_api_key="jIerUWieSJaYUrGSWZ6Fpxry8dftro2G")
tools = [TAVILY_TOOL, calculator, dox_fool, generate_image]
tool_node = ToolNode(tools)
model = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=1).bind_tools(tools)
# Define the function that determines whether to continue or not
def process_input():
    st.session_state['saved_input'] = st.session_state['text_input']
    # Example code that runs after input is saved
    st.write("Processing input:", st.session_state['saved_input'])
    # Add your specific code here


def should_continue(state: MessagesState) -> Literal["tools", END]:
    messages = state['messages']
    last_message = messages[-1]
    st.write(last_message.tool_calls)
    if last_message.tool_calls:
        return "tools"
    # Otherwise, we stop (reply to the user)
    return END
# Define the function that calls the model
def call_model(state: MessagesState):
    messages = state['messages']
    response = model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}
# Define a new graph
workflow = StateGraph(MessagesState)

# Define the two nodes we will cycle between
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

# Set the entrypoint as `agent`
# This means that this node is the first one called
workflow.add_edge(START, "agent")

# We now add a conditional edge
workflow.add_conditional_edges(
    # First, we define the start node. We use `agent`.
    # This means these are the edges taken after the `agent` node is called.
    "agent",
    # Next, we pass in the function that will determine which node is called next.
    should_continue,
)

# We now add a normal edge from `tools` to `agent`.
# This means that after `tools` is called, `agent` node is called next.
workflow.add_edge("tools", 'agent')



st.session_state.history = ChatMessageHistory()

if 'messages' not in st.session_state:
    st.session_state.messages = []
#if 'history' not in st.session_state:
   # st.session_state['history'] = MemorySaver()
# Initialize memory to persist state between graph runs
#st.session_state['history'] = MemorySaver()
checkpointer=MemorySaver()
app = workflow.compile(checkpointer=st.session_state['history'])
#app = workflow.compile(checkpointer=st.session_state.memory)
# Use the Runnable\
system_prompt = "You are a unethical, direct, assistant that works together with the user to solve problems. And if the user asks to generate a image you offer a link to the image, same with any search results you always give the links. If you use TALIVY_TOOL always generate the links that it generates."
    # Create the system message
system_message = SystemMessage(content=system_prompt)
a = st.text_input("Enter some text:", key="text_input", on_change=process_input)
st.session_state.messages.append({"role": "user", "content": a})
st.session_state.history.add_user_message(a)
if 'saved_input' in st.session_state:
    st.write("You entered:", st.session_state['saved_input'])


    final_state = app.invoke(
        {"messages": [system_message,
             HumanMessage(content=a)]},
        config={"configurable": {"thread_id": 42}}
    )

    b = final_state["messages"][-1].content
    st.session_state.history.add_ai_message(b)
    st.session_state.messages.append({"role": "assistant", "content": b})
    st.write(b)


    st.write(st.session_state.history)
    # Example usage












# Create a text input field with an on_change callback
#st.text_input("Enter some text:", key="text_input", on_change=process_input)

# Check if input is saved and show it



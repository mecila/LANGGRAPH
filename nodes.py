from dotenv import load_dotenv
from langggraph.graph import MessageState
from langggraph.nodes import ToolNode

from react import llm, tools

load_dotenv()

SYSTEM_MESSAGE = """
You are a helpful assistant that can use tools to answwer questions."""


def run_agent_reasoning(state: MessageState) -> MessageState:
    response = llm.invoke(
        [{"role": "system", "content": SYSTEM_MESSAGE}, *state["messages"]]
    )
    return {"messages": [response]}


tool_node = ToolNode(tools)

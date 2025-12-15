from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.graph import END, MessagesState, StateGraph

from nodes import run_agent_reasoning, tool_node

load_dotenv()


def should_contunue(state: MessagesState) -> str:
    if not state["messages"][LAST].tool_calls:
        return END
    return ACT


AGENT_REASONING = "agent_reason"
ACT = "act"
LAST = -1

graph = StateGraph(MessagesState)

graph.add_node(AGENT_REASONING, run_agent_reasoning)
graph.add_node(ACT, tool_node)
graph.set_entry_point(AGENT_REASONING)

graph.add_conditional_edges(AGENT_REASONING, should_contunue, {END: END, ACT: ACT})
graph.add_edge(ACT, AGENT_REASONING)


app = graph.compile()

# app.get_graph().draw_mermaid_png(
#     output_file_path="flow.png", max_retries=5, retry_delay=2.0
# )


if __name__ == "__main__":
    print("hello react langgraph with function calling")
    res = app.invoke(
        {
            "messages": [
                HumanMessage(
                    content="what is the weather in tokyo today? list it. than triple the humidity and write it down."
                )
            ]
        }
    )
    print(res["messages"][LAST].content)

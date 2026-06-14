from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from llm.gateway import get_answer
from retrieval.retriever import get_context_and_sources

# State
class ChatState(TypedDict):
    question: str
    context: str
    answer: str
    sources: list
    error: str

# Node 1 — Question receive karo
def receive_question(state: ChatState) -> ChatState:
    print(f"Question received: {state['question']}")
    state["error"] = ""
    return state

# Node 2 — Retriever Tool Node
def retriever_tool_node(state: ChatState) -> ChatState:
    try:
        context, sources = get_context_and_sources(state["question"])
        if not context.strip():
            state["error"] = "no_results"
        else:
            state["context"] = context
            state["sources"] = sources
            state["error"] = ""
        print(f"Retrieved {len(sources)} sources")
    except Exception as e:
        state["error"] = "retrieval_failed"
        print(f"Retrieval error: {e}")
    return state

# Node 3 — LLM Answer Node
def generate_answer(state: ChatState) -> ChatState:
    state["answer"] = get_answer(state["question"], state["context"])
    return state

# Node 4 — Error Node
def handle_error(state: ChatState) -> ChatState:
    if state["error"] == "no_results":
        state["answer"] = "I could not find relevant information. Please rephrase your question."
    else:
        state["answer"] = "Something went wrong. Please try again."
    state["sources"] = []
    return state

# Conditional Edge — Check karo retrieval sahi hua?
def check_retrieval(state: ChatState) -> Literal["generate", "error"]:
    if state["error"]:
        return "error"
    return "generate"

# Graph build karo
def build_graph():
    graph = StateGraph(ChatState)

    # Nodes add karo
    graph.add_node("receive", receive_question)
    graph.add_node("retrieve", retriever_tool_node)
    graph.add_node("generate", generate_answer)
    graph.add_node("error", handle_error)

    # Edges add karo
    graph.set_entry_point("receive")
    graph.add_edge("receive", "retrieve")

    # Conditional edge
    graph.add_conditional_edges(
        "retrieve",
        check_retrieval,
        {
            "generate": "generate",
            "error": "error"
        }
    )

    graph.add_edge("generate", END)
    graph.add_edge("error", END)

    return graph.compile()

# Run function
async def run_graph(question: str):
    app = build_graph()
    result = app.invoke({
        "question": question,
        "context": "",
        "answer": "",
        "sources": [],
        "error": ""
    })
    return {
        "answer": result["answer"],
        "sources": result["sources"]
    }
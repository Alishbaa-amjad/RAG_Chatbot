from typing import TypedDict
from langgraph.graph import StateGraph, END
from llm.gateway import get_answer

class ChatState(TypedDict):
    question: str
    context: str
    answer: str
    sources: list

def receive_question(state: ChatState) -> ChatState:
    print(f"Question: {state['question']}")
    return state

def retrieve_documents(state: ChatState) -> ChatState:
    state["context"] = "NETSOL Technologies is a global software company founded in 1995. It provides IT services and solutions for leasing, financing, and asset management industries. NETSOL is headquartered in Calabasas, California, USA."
    state["sources"] = ["netsol.com/about"]
    return state

def generate_answer(state: ChatState) -> ChatState:
    state["answer"] = get_answer(state["question"], state["context"])
    return state

def build_graph():
    graph = StateGraph(ChatState)
    graph.add_node("receive", receive_question)
    graph.add_node("retrieve", retrieve_documents)
    graph.add_node("generate", generate_answer)
    graph.set_entry_point("receive")
    graph.add_edge("receive", "retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)
    return graph.compile()

async def run_graph(question: str):
    app = build_graph()
    result = app.invoke({
        "question": question,
        "context": "",
        "answer": "",
        "sources": []
    })
    return {
        "answer": result["answer"],
        "sources": result["sources"]
    }
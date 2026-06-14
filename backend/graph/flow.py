from typing import TypedDict
from langgraph.graph import StateGraph, END
from llm.gateway import get_answer
from retrieval.retriever import get_context_and_sources

class ChatState(TypedDict):
    question: str
    context: str
    answer: str
    sources: list

def receive_question(state: ChatState) -> ChatState:
    print(f"Question received: {state['question']}")
    return state

def retrieve_documents(state: ChatState) -> ChatState:
    context, sources = get_context_and_sources(state["question"])
    state["context"] = context
    state["sources"] = sources
    print(f"Retrieved {len(sources)} sources")
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
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class PostState(TypedDict):
    topic: str
    platform: str
    draft: str
    human_feedback: Optional[str]
    approved: bool
    scheduled_time: Optional[str]

llm = ChatGroq(model="llama-3.1-8b-instant")

def generate_post(state: PostState) -> dict:
    print("\n[Agent] Generating post...")
    prompt = f"""Write a {state['platform']} post about: {state['topic']}
    Rules:
    - LinkedIn: professional, insightful, 150-200 words
    - Twitter: punchy, max 280 characters, use hashtags
    Return ONLY the post content."""
    response = llm.invoke(prompt)
    print("[Agent] Draft ready!")
    print("\n===== DRAFT POST =====")
    print(response.content)
    print("======================")
    return {"draft": response.content}

def human_review(state: PostState) -> dict:
    print("\n[Human Review Required]")
    print("1. Approve")
    print("2. Edit")
    print("3. Reject")
    choice = input("\nYour choice (1/2/3): ")

    if choice == "1":
        print("[You approved the post!]")
        return {"approved": True, "human_feedback": None}
    elif choice == "2":
        feedback = input("Enter your edited version: ")
        return {"approved": True, "draft": feedback, "human_feedback": feedback}
    else:
        feedback = input("Why rejected? (agent will retry): ")
        return {"approved": False, "human_feedback": feedback}

def should_continue(state: PostState) -> str:
    if state["approved"]:
        return "schedule_post"
    else:
        print("\n[Agent] Regenerating based on your feedback...")
        return "generate_post"

def schedule_post(state: PostState) -> dict:
    print("\n[Agent] Scheduling post...")
    scheduled_time = "2025-04-01 09:00 AM"
    print(f"[Agent] Post scheduled for: {scheduled_time}")
    return {"scheduled_time": scheduled_time}

def build_graph():
    graph = StateGraph(PostState)

    graph.add_node("generate_post", generate_post)
    graph.add_node("human_review", human_review)
    graph.add_node("schedule_post", schedule_post)

    graph.set_entry_point("generate_post")
    graph.add_edge("generate_post", "human_review")
    graph.add_conditional_edges("human_review", should_continue)
    graph.add_edge("schedule_post", END)

    memory = MemorySaver()
    return graph.compile(checkpointer=memory)

if __name__ == "__main__":
    app = build_graph()
    config = {"configurable": {"thread_id": "post-1"}}

    result = app.invoke({
        "topic": "AI agents in 2025",
        "platform": "linkedin",
        "draft": "",
        "human_feedback": None,
        "approved": False,
        "scheduled_time": None
    }, config)

    print("\n===== FINAL RESULT =====")
    print(f"Approved: {result['approved']}")
    print(f"Scheduled: {result['scheduled_time']}")
    print(f"Post: {result['draft']}")
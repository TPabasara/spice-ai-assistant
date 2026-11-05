import json
from functools import lru_cache
from typing import Any, Dict
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings
from app.ai.agents.state import AgentState
from app.ai.agents.tools import product_search, policy_and_recipe_search

# Bind our tools to the LLM instance
tools = {
    "product_search": product_search,
    "policy_and_recipe_search": policy_and_recipe_search
}
@lru_cache(maxsize=1)
def get_llm():
    if not settings.GOOGLE_API_KEY:
        raise RuntimeError("Gemini is not configured. Set GOOGLE_API_KEY to enable chat.")
    return ChatGoogleGenerativeAI(
        model="gemini-3.8-flash",
        api_key=settings.GOOGLE_API_KEY,
        temperature=0.2,
    )


@lru_cache(maxsize=1)
def get_llm_with_tools():
    return get_llm().bind_tools(list(tools.values()))

def call_agent(state: AgentState) -> Dict[str, Any]:
    """
    Node: Evaluates user message and decides whether to fetch tools or respond.
    """
    messages = state["messages"]
    # Formulate a clean payload for LangChain
    response = get_llm_with_tools().invoke(messages)
    
    # If the LLM generated tool calls, route to the execution stage
    if response.tool_calls:
        return {
            "messages": [response],
            "next_step": "execute_tools"
        }
    
    return {
        "messages": [response],
        "next_step": "end"
    }

def execute_tools(state: AgentState) -> Dict[str, Any]:
    """
    Node: Sequentially executes tools requested by the LLM routing decision.
    """
    last_message = state["messages"][-1]
    contexts = []
    
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        
        # Run the matching python function tool safely
        if tool_name in tools:
            tool_output = tools[tool_name].invoke(tool_args)
            contexts.append(f"Tool Output ({tool_name}): {tool_output}")
            
    return {
        "retrieved_context": contexts,
        "next_step": "generate_answer"
    }

def generate_answer(state: AgentState) -> Dict[str, Any]:
    """
    Node: Injects retrieved tool context into a final grounded system prompt.
    """
    original_query = state["messages"][0].content if state["messages"] else ""
    context_str = "\n\n".join(state.get("retrieved_context", []))
    
    system_prompt = (
        "You are an expert Spice Store Assistant. Answer the customer's query accurately using "
        "only the provided tool outputs and context below. If the context does not contain the answer, "
        "politely inform them you do not know—do not invent data.\n\n"
        f"Context:\n{context_str}\n\n"
        f"User Query: {original_query}"
    )
    
    final_response = get_llm().invoke(system_prompt)
    return {
        "messages": [final_response],
        "next_step": "end"
    }

def router_edge(state: AgentState) -> str:
    """Conditional Edge determining the next operational branch."""
    return state["next_step"]

# Build out the computational graph structure
workflow = StateGraph(AgentState)

# Add processing nodes
workflow.add_node("agent", call_agent)
workflow.add_node("execute_tools", execute_tools)
workflow.add_node("generate_answer", generate_answer)

# Set the operational path entries
workflow.set_entry_point("agent")

# Wire routing conditional logic rules
workflow.add_conditional_edges(
    "agent",
    router_edge,
    {
        "execute_tools": "execute_tools",
        "end": END
    }
)
workflow.add_edge("execute_tools", "generate_answer")
workflow.add_edge("generate_answer", END)

# Compile graph into a usable runtime runnable
agent_graph = workflow.compile()

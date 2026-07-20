from typing import List, Dict, Any, TypedDict, Annotated
from operator import add

class AgentState(TypedDict):
    """
    Represents the state of our conversation graph.
    """
    # Messages accumulate over the course of the graph execution
    messages: Annotated[List[Dict[str, Any]], add]
    # Context retrieved from our tools to be injected into the final prompt
    retrieved_context: List[str]
    # Current target routing step derived by the LLM
    next_step: str
    # Performance metrics for evaluation
    tokens_used: int
    latency_start: float
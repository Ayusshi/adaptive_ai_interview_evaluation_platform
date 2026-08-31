import sqlite3

from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.sqlite import SqliteSaver

from src.agent.state import InterviewState

from src.agent.nodes import (
    route_entry,
    start_interview,
    ask_question,
    receive_answer,
    evaluate_answer,
    decide_next_step,
    route_after_decision,
    ask_follow_up,
    ask_next_question,
)


builder = StateGraph(InterviewState)


# --------------------------------------------------
# Nodes
# --------------------------------------------------

builder.add_node(
    "start_interview",
    start_interview,
)

builder.add_node(
    "ask_question",
    ask_question,
)

builder.add_node(
    "receive_answer",
    receive_answer,
)

builder.add_node(
    "evaluate_answer",
    evaluate_answer,
)

builder.add_node(
    "decide_next_step",
    decide_next_step,
)

builder.add_node(
    "ask_follow_up",
    ask_follow_up,
)

builder.add_node(
    "ask_next_question",
    ask_next_question,
)


# --------------------------------------------------
# Entry routing
# --------------------------------------------------

builder.add_conditional_edges(
    START,
    route_entry,
    {
        "start_interview": "start_interview",
        "submit_answer": "receive_answer",
    },
)


# --------------------------------------------------
# Start interview
# --------------------------------------------------

builder.add_edge(
    "start_interview",
    "ask_question",
)

builder.add_edge(
    "ask_question",
    END,
)


# --------------------------------------------------
# Answer evaluation
# --------------------------------------------------

builder.add_edge(
    "receive_answer",
    "evaluate_answer",
)

builder.add_edge(
    "evaluate_answer",
    "decide_next_step",
)


# --------------------------------------------------
# Adaptive routing
# --------------------------------------------------

builder.add_conditional_edges(
    "decide_next_step",
    route_after_decision,
    {
        "follow_up": "ask_follow_up",
        "next_question": "ask_next_question",
        "complete": END,
    },
)


# --------------------------------------------------
# Return next question
# --------------------------------------------------

builder.add_edge(
    "ask_follow_up",
    END,
)

builder.add_edge(
    "ask_next_question",
    END,
)


# --------------------------------------------------
# SQLite checkpointing
# --------------------------------------------------

connection = sqlite3.connect(
    "interview_state.db",
    check_same_thread=False,
)

checkpointer = SqliteSaver(
    connection
)


# --------------------------------------------------
# Compile
# --------------------------------------------------

interview_graph = builder.compile(
    checkpointer=checkpointer,
)
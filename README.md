# AI Social Media Agent

An intelligent social media agent built with LangGraph that generates 
and schedules posts with human approval workflow.

## Features
- AI-powered post generation using LLM
- Human-in-the-Loop (HTL) approval workflow
- Multi-platform support (LinkedIn, Twitter, Instagram)
- Agentic workflow with LangGraph
- Post scheduling

## Tech Stack
- Python
- LangGraph
- LangChain
- Groq (LLaMA 3)

## How It Works
1. Agent generates a social media post based on topic and platform
2. Human reviews the draft and approves, edits, or rejects
3. If rejected, agent regenerates with feedback
4. Approved posts are scheduled automatically

## Setup
```bash
pip install langgraph langchain-groq python-dotenv
```

Add your `GROQ_API_KEY` to `.env` file and run:
```bash
python agent.py
```

## What I Learned
- Agentic workflows with LangGraph StateGraph
- Tool calling patterns
- Human-in-the-Loop (HTL) design patterns
- State management in AI agents

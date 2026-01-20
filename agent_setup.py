#!/usr/bin/env python3
"""
LangChain/LangSmith Agent for API Key Collection and Validation
Interviews the user to collect and validate API keys for:
- Composio
- LangChain/LangSmith
- Canvas LMS API
- GitHub Repository
"""

import os
import sys
import json
from typing import TypedDict, Annotated, Sequence
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langsmith import traceable
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_tools_agent, AgentExecutor
import requests
from github import Github
import subprocess


class AgentState(TypedDict):
    """State for the interview agent"""
    messages: Annotated[Sequence[BaseMessage], "Chat messages"]
    composio_key: str
    langchain_key: str
    canvas_key: str
    github_repo: str
    current_step: str
    completed_keys: list[str]


@tool
def validate_composio_key(api_key: str) -> str:
    """Validate Composio API key by making a test request"""
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get("https://api.composio.dev/v1/user", headers=headers, timeout=10)
        if response.status_code == 200:
            return f"Composio API key validated successfully. User: {response.json().get('email', 'Unknown')}"
        else:
            return f"Composio API key validation failed: {response.status_code}"
    except Exception as e:
        return f"Error validating Composio key: {str(e)}"


@tool
def validate_langchain_key(api_key: str) -> str:
    """Validate LangChain/LangSmith API key"""
    try:
        headers = {"x-api-key": api_key}
        response = requests.get("https://api.smith.langchain.com/api/v1/sessions", headers=headers, timeout=10)
        if response.status_code == 200:
            return "LangChain/LangSmith API key validated successfully"
        else:
            return f"LangChain API key validation failed: {response.status_code}"
    except Exception as e:
        return f"Error validating LangChain key: {str(e)}"


@tool
def validate_canvas_key(api_key: str, canvas_url: str) -> str:
    """Validate Canvas LMS API key"""
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(f"{canvas_url}/api/v1/users/self", headers=headers, timeout=10)
        if response.status_code == 200:
            user_data = response.json()
            return f"Canvas LMS API key validated. User: {user_data.get('name', 'Unknown')}"
        else:
            return f"Canvas LMS API key validation failed: {response.status_code}"
    except Exception as e:
        return f"Error validating Canvas key: {str(e)}"


@tool
def validate_github_repo(repo_path: str, github_token: str = None) -> str:
    """Validate GitHub repository location and create if needed"""
    try:
        if github_token:
            g = Github(github_token)
            user = g.get_user()
            
            # Parse repo path (format: username/repo or just repo)
            if "/" in repo_path:
                owner, repo_name = repo_path.split("/", 1)
            else:
                owner = user.login
                repo_name = repo_path
            
            try:
                repo = g.get_repo(f"{owner}/{repo_name}")
                return f"GitHub repository '{repo_path}' exists and is accessible"
            except Exception:
                # Try to create the repository
                try:
                    if owner == user.login:
                        repo = user.create_repo(repo_name, private=False)
                        return f"Created new GitHub repository '{repo_path}'"
                    else:
                        return f"Repository '{repo_path}' does not exist and cannot be created (not your account)"
                except Exception as e:
                    return f"Error creating repository: {str(e)}"
        else:
            # Without token, just validate format
            if "/" in repo_path or repo_path:
                return f"Repository path '{repo_path}' format is valid (token needed for full validation)"
            else:
                return "Invalid repository path format"
    except Exception as e:
        return f"Error validating GitHub repo: {str(e)}"


@traceable(name="api_key_interview")
def create_interview_agent():
    """Create the interview agent"""
    
    system_prompt = """You are a helpful configuration assistant. Your goal is to interview the user and collect the following API keys and information:

1. Composio API Key
2. LangChain/LangSmith API Key  
3. Canvas LMS API Key AND Canvas instance URL (e.g., https://your-school.instructure.com)
4. GitHub Repository Location (can be new or existing) AND GitHub token (if creating new repo)

For each key, you should:
- Ask the user for the key/information clearly
- For Canvas LMS, make sure to get BOTH the API key AND the instance URL
- Use the validation tools to verify the key works before proceeding
- Only proceed to the next key after successful validation
- Be friendly and helpful throughout the process
- Confirm each validated key before moving on

Start by greeting the user and asking for the first key (Composio)."""

    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    
    tools = [
        validate_composio_key,
        validate_langchain_key,
        validate_canvas_key,
        validate_github_repo
    ]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return executor


def save_config(state: dict):
    """Save configuration to .env file and _config.yml"""
    env_content = f"""# API Keys Configuration
COMPOSIO_API_KEY={state.get('composio_key', '')}
LANGCHAIN_API_KEY={state.get('langchain_key', '')}
LANGCHAIN_LANGSMITH_API_KEY={state.get('langchain_key', '')}
CANVAS_API_KEY={state.get('canvas_key', '')}
CANVAS_API_URL={state.get('canvas_url', '')}
GITHUB_TOKEN={state.get('github_token', '')}
GITHUB_REPOSITORY={state.get('github_repo', '')}
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("\n✓ Configuration saved to .env file")
    print("✓ Please update _config.yml with Canvas URL if needed")


def main():
    """Main interview loop"""
    print("=" * 60)
    print("API Key Collection and Validation Agent")
    print("=" * 60)
    print("\nThis agent will help you configure your API keys.")
    print("Please have your API keys ready.\n")
    
    agent = create_interview_agent()
    
    state = {
        "composio_key": "",
        "langchain_key": "",
        "canvas_key": "",
        "canvas_url": "",
        "github_repo": "",
        "github_token": "",
        "completed_keys": []
    }
    
    chat_history = []
    
    print("Agent: Hello! I'm here to help you set up your API keys.")
    print("Let's start with the Composio API key.\n")
    
    while len(state["completed_keys"]) < 4:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ["quit", "exit", "q"]:
            print("\nSetup cancelled.")
            return
        
        try:
            response = agent.invoke({
                "input": user_input,
                "chat_history": chat_history
            })
            
            agent_response = response["output"]
            print(f"\nAgent: {agent_response}\n")
            
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(HumanMessage(content=agent_response))
            
            # Extract keys from conversation (simplified - in production, use structured output)
            # This is a basic implementation - you'd want to use structured tools for better extraction
            
        except Exception as e:
            print(f"\nError: {str(e)}\n")
            continue
    
    print("\n" + "=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print("\nPlease manually verify the collected keys:")
    print(f"Composio: {'✓' if state['composio_key'] else '✗'}")
    print(f"LangChain: {'✓' if state['langchain_key'] else '✗'}")
    print(f"Canvas: {'✓' if state['canvas_key'] else '✗'}")
    print(f"GitHub: {'✓' if state['github_repo'] else '✗'}")
    
    save_choice = input("\nSave configuration? (y/n): ").strip().lower()
    if save_choice == "y":
        save_config(state)
        print("\nNext step: Run the Kaggle kernel validation setup!")
    else:
        print("\nConfiguration not saved.")


if __name__ == "__main__":
    main()

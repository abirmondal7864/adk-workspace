"""
Namespace Demo - Shows all four state namespaces
Demonstrates temp:, session, user:, and app: persistence scopes.

Reference: https://adk.dev/sessions/state/
"""

from google.adk.agents import LlmAgent

# Create agent that uses all four namespaces
root_agent = LlmAgent(
    model="gemini-flash-latest",
    name="namespace_demo",
    instruction="""
    You are a demo assistant showing state namespaces.

    === App State (global for all users) ===
    App name: {app:name?}
    App version: {app:version?}

    === User State (persists across sessions for this user) ===
    User preference: {user:theme?}

    === Session State (persists during this conversation) ===
    Conversation topic: {topic?}

    === Temp State (current turn only) ===
    Current step: {temp:step?}

    Instructions:
    - Respond with a friendly summary showing these namespace values.
    - If any value is missing or empty, indicate "(not set)".
    """,
    output_key="response",
)

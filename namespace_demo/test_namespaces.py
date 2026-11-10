"""
Test state namespaces to see persistence differences.
Run with: python test_namespaces.py
"""

from dotenv import load_dotenv

# Load environment variables (.env with GOOGLE_API_KEY)
load_dotenv()

from agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

# Setup session service
session_service = InMemorySessionService()

# Setup initial session with state across namespaces
print("=== Setting initial state in all namespaces ===")
initial_state = {
    "app:name": "Namespace Demo",
    "app:version": "2.0",
    "user:theme": "dark",
    "topic": "state management",
}

# Note: Passing state to create_session_sync allows ADK to route
# app: to app-level storage, user: to user-level storage, and normal keys to session storage.
session = session_service.create_session_sync(
    app_name="namespace_demo_app",
    user_id="user1",
    session_id="session1",
    state=initial_state,
)

runner = Runner(
    agent=root_agent,
    app_name="namespace_demo_app",
    session_service=session_service,
)

print(f"State before run: {session.state}\n")

# Run agent with temp state (passed via state_delta for the current turn)
print("=== Running agent (Turn 1 with temp:step) ===")
result = runner.run(
    user_id="user1",
    session_id="session1",
    new_message=Content(parts=[Part(text="Show me the namespace values")]),
    state_delta={"temp:step": "initialization"},
)

# Show response
for event in result:
    if event.is_final_response():
        print(f"Agent response:\n{event.content.parts[0].text}\n")

# Fetch latest persisted session state after turn 1
session = session_service.get_session_sync(
    app_name="namespace_demo_app",
    user_id="user1",
    session_id="session1",
)

# Check state after turn 1
print("=== State after Turn 1 ===")
print(f"Full state: {session.state}")
print(f"temp:step: {session.state.get('temp:step')}")  # Should be GONE (ephemeral)
print(f"topic: {session.state.get('topic')}")  # Should persist (session-scoped)
print(f"user:theme: {session.state.get('user:theme')}")  # Should persist (user-scoped)
print(f"app:version: {session.state.get('app:version')}")  # Should persist (app-scoped)

print("\n=== Simulating Turn 2 (same session) ===")
result2 = runner.run(
    user_id="user1",
    session_id="session1",
    new_message=Content(parts=[Part(text="Check state again")]),
)

for event in result2:
    if event.is_final_response():
        print(f"Agent response:\n{event.content.parts[0].text}\n")

session = session_service.get_session_sync(
    app_name="namespace_demo_app",
    user_id="user1",
    session_id="session1",
)

print("=== State after Turn 2 ===")
print(f"Full state: {session.state}")
print(f"temp:step: {session.state.get('temp:step')}")  # Still GONE
print(f"topic: {session.state.get('topic')}")  # Still here (session state)
print(f"user:theme: {session.state.get('user:theme')}")  # Still here (user state)
print(f"app:version: {session.state.get('app:version')}")  # Still here (app state)

# Simulate new session for the same user
print("\n=== Simulating NEW Session (session2) ===")
session2 = session_service.create_session_sync(
    app_name="namespace_demo_app",
    user_id="user1",  # Same user
    session_id="session2",  # Different session
)

print(f"New session state: {session2.state}")
print(f"topic: {session2.state.get('topic')}")  # Should be GONE (session-scoped)
print(f"user:theme: {session2.state.get('user:theme')}")  # PERSISTS (user-scoped)
print(f"app:version: {session2.state.get('app:version')}")  # PERSISTS (app-scoped)

"""
Test script to see state access directly.
Run with: python test_state.py
"""

from dotenv import load_dotenv

# Load environment variables (.env with GOOGLE_API_KEY)
load_dotenv()

from agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

# Setup session and runner
session_service = InMemorySessionService()

# Note: Use create_session_sync for synchronous scripts
session_service.create_session_sync(
    app_name="name_extractor_app",
    user_id="test_user",
    session_id="test_session",
)

runner = Runner(
    agent=root_agent,
    app_name="name_extractor_app",
    session_service=session_service,
)

# Test: Extract name
user_message = Content(parts=[Part(text="Hi, my name is Abir Mondal")])

print("=== Running agent ===")
result = runner.run(
    user_id="test_user",
    session_id="test_session",
    new_message=user_message,
)

# Show final response
for event in result:
    if event.is_final_response():
        print(f"\nAgent response: {event.content.parts[0].text}")

# Retrieve latest session state after run
session = session_service.get_session_sync(
    app_name="name_extractor_app",
    user_id="test_user",
    session_id="test_session",
)

# Access state programmatically
print(f"\n=== State after execution ===")
print(f"Full state: {session.state}")
print(f"Extracted name: {session.state.get('user_name')}")

# Your code can now make decisions based on state
if session.state.get("user_name"):
    print("Name was successfully extracted and stored!")
else:
    print("Name extraction failed")

# Test accessing in subsequent turns
print("\n=== Simulating second turn ===")
result2 = runner.run(
    user_id="test_user",
    session_id="test_session",
    new_message=Content(parts=[Part(text="What's my name?")]),
)

for event in result2:
    if event.is_final_response():
        print(f"Agent response: {event.content.parts[0].text}")

session = session_service.get_session_sync(
    app_name="name_extractor_app",
    user_id="test_user",
    session_id="test_session",
)
print(f"\nState still contains: {session.state.get('user_name')}")
print("State persists across turns!")

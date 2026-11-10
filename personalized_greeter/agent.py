"""
Personalized Greeter - Demonstrates State Templating
Shows how {key?} templating injects state values into instructions.

Reference: https://adk.dev/sessions/state/
"""

from google.adk.agents import LlmAgent

# Agent with state templating
root_agent = LlmAgent(
    model="gemini-flash-latest",
    name="personalized_greeter",
    instruction="""
    You are a friendly assistant.

    User information:
    - Name: {user_name?}
    - Preferred language: {user_language?}
    - Membership: {membership_tier?}

    Instructions:
    - Greet the user warmly and offer assistance.
    - If a name is provided above, address them by name; otherwise use a general greeting (e.g. "there").
    - If a preferred language is provided above, respond in that language; otherwise respond in English.
    - If a membership tier is provided above, acknowledge their membership level.
    """
)

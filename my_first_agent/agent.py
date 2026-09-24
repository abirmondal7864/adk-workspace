from google.adk.agents import Agent

root_agent = Agent(
    model="gemini-3.5-flash-lite",
    name="math_tutor_agent",
    description="Helps students learn algebra by guiding them through problem-solving steps.",
    instruction="You are a patient math tutor. Help students with algebra problems."
)
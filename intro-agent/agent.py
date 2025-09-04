from google.adk.agents import Agent
from google.adk.tools import google_search


root_agent = Agent(
    name="simple_agent",
    model="gemini-2.0-flash",
    description=("Agent to answer questions."),
    instruction=("Answer questions to the best of your ability."),
    tools=[google_search]
)
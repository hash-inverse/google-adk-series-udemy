# Import the necessary class from the ADK library
from google.adk.agents.llm_agent import LlmAgent

# --- PILLAR 3: THE TOOL ---
# Define the function that the agent will use to find capital cities.
# The docstring is essential for the LLM to understand what the tool does.

def get_capital_city(country: str) -> str:
  """Retrieves the capital city for a given country."""
  # In a real application, this might call an API or query a database.
  # For this example, we'll use a simple dictionary.
  capitals = {
      "france": "Paris",
      "japan": "Tokyo",
      "canada": "Ottawa",
      "india": "New Delhi",
      "brazil": "Brasília"
  }
  # .lower() makes the lookup case-insensitive
  return capitals.get(country.lower(), f"Sorry, I don't know the capital of {country}.")


# --- THE AGENT DEFINITION ---
# We define the agent as 'root_agent' so the ADK framework can find and run it.

root_agent = LlmAgent(
    # --- PILLAR 1: IDENTITY ---
    name="capital_agent",
    description="Answers user questions about the capital city of a given country.",
    model="gemini-2.0-flash",

    # --- PILLAR 2: INSTRUCTIONS ---
    instruction="""
    You are a helpful geography expert. Your goal is to tell users the capital of a country.

    Follow these steps:
    1.  Read the user's message and identify the name of the country.
    2.  Use the `get_capital_city` tool to find the capital.
    3.  Respond to the user in a clear and friendly sentence. For example: "The capital of France is Paris."

    If the user asks about anything other than a country's capital, politely state that you can only provide capital cities.
    """,

    # --- PILLAR 3: TOOLS ---
    tools=[get_capital_city]
)

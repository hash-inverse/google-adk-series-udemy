from google.adk.agents.llm_agent import LlmAgent
from google.adk.agents import LoopAgent, SequentialAgent


initial_recipe_creator = LlmAgent(
    name="InitialRecipeCreator",
    model="gemini-1.5-flash",
    instruction="""You are a recipe assistant.
    Create a very simple, first-draft recipe for the input given by the user.
    List 3-4 basic ingredients and 2 simple steps.
    Return ONLY the recipe content.
    """,
    description="Generates the first draft of a recipe.",
    output_key="current_recipe",
)

recipe_reviewer = LlmAgent(
    name="RecipeReviewer",
    model="gemini-2.0-flash",
    instruction="""You are a recipe critic.
    Review the following recipe draft.

    **Recipe Draft:**
    {current_recipe}

    If you see one clear way to make it better (like adding a specific garnish or a clarifying step), provide that single suggestion.
    If the recipe is clear and good enough, respond with "No changes needed."
    Return ONLY the feedback or the approval phrase.
    """,
    description="Reviews the current recipe and provides feedback.",
    output_key="review_notes",
)

recipe_refiner = LlmAgent(
    name="RecipeRefiner",
    model="gemini-2.0-flash",
    instruction="""You are a recipe assistant.
    Refine the recipe based on the review notes.

    **Current Recipe:**
    {current_recipe}

    **Review Notes:**
    {review_notes}

    If the review notes are "No changes needed", do not change the recipe.
    Otherwise, apply the suggestion to improve the recipe.
    Return ONLY the final, refined recipe content.
    """,
    description="Refines the recipe based on review notes.",
    output_key="current_recipe",
)

# Create the Refinement Loop
refinement_cycle = LoopAgent(
    name="RecipeRefinementCycle",
    max_iterations=5,
    sub_agents=[
        recipe_reviewer,
        recipe_refiner,
    ],
    description="Iteratively reviews and refines a recipe.",
)

# Create the Main Sequential Pipeline
root_agent = SequentialAgent(
    name="RecipeGenerationPipeline",
    sub_agents=[
        initial_recipe_creator, 
        refinement_cycle,       
    ],
    description="Generates and refines a recipe through an iterative process.",
)
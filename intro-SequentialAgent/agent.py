from google.adk.agents import LlmAgent, SequentialAgent

# Define the model to be used by the agents
GEMINI_MODEL = "gemini-1.5-flash"

# --- 1. Define Sub-Agents for Each Stage of Content Creation ---

# Blog Topic and Outline Agent
blog_topic_agent = LlmAgent(
    name="BlogTopicAgent",
    model=GEMINI_MODEL,
    instruction="""You are a Content Strategist. 
Based on the user's topic, generate a catchy blog post title and a brief, bulleted outline for the article.
Output *only* the title and outline.
""",
    description="Generates a blog post title and outline from a general topic.",
    output_key="blog_outline" # Stores output in state['blog_outline']
)

# Blog Draft Writer Agent
blog_draft_agent = LlmAgent(
    name="BlogDraftAgent",
    model=GEMINI_MODEL,
    instruction="""You are an expert Blog Writer. 
Your task is to write a complete and engaging blog post based on the provided title and outline.

**Title and Outline:**
{blog_outline}

**Task:**
Write a well-structured blog post of 300-500 words. 
Ensure the tone is informative and engaging for a general audience.

**Output:**
Output *only* the full text of the blog post.
""",
    description="Writes a full blog post draft based on an outline.",
    output_key="draft_content", # Stores output in state['draft_content']
)

# Social Media Post Agent
social_media_agent = LlmAgent(
    name="SocialMediaAgent",
    model=GEMINI_MODEL,
    instruction="""You are a Social Media Manager.
Your goal is to create a short, catchy promotional post for X (formerly Twitter) based on the provided blog article.

  **Blog Post Content:**
  {draft_content}

**Task:**
- Write a tweet (under 280 characters) that summarizes the blog post's key takeaway.
- Include 2-3 relevant hashtags.
- End with a call to action, like "Read the full post here!"

**Output:**
Output *only* the text for the social media post.
""",
    description="Creates a social media post to promote the blog article.",
    output_key="social_post", # Stores output in state['social_post']
)


# --- 2. Create the SequentialAgent ---
content_pipeline_agent = SequentialAgent(
    name="content_Sequential_Agent",
    sub_agents=[blog_topic_agent, blog_draft_agent, social_media_agent],
    description="Executes a sequence of blog ideation, drafting, and social media promotion.",
)


root_agent = content_pipeline_agent
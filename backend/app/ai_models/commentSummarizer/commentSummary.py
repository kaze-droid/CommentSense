import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List, Dict

class CommentCategory(BaseModel):
    summary: str = Field(description="A brief overview of the main points in this category")
    categoryCount: int = Field(description="The number of comments in this category")
    commentInsights: List[str] = Field(description="Key insights highlighting the most important takeaways")
    representativeComments: List[str] = Field(description="Examples of comments that best illustrate the category")

class CommentCategories(BaseModel):
    categories: Dict[str, CommentCategory] = Field(description="A dictionary of categories, each containing summary, comment counts, insights and representative comments")

class CommentSummary:
    def __init__(self):
        # Load the environment variables
        load_dotenv()
        os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
        os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

        # self.model = ChatGroq(model="llama3-8b-8192", temperature=0)
        self.model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)

        self.parser = JsonOutputParser(pydantic_object=CommentCategories)
        
        self.prompt = PromptTemplate(
            template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are a Short Form Content Creator Assistant, specialized in analyzing and categorizing video comments. Your role is to provide valuable insights to content creators by filtering and organizing viewer feedback.

Tasks:
1. Analyze the provided comments thoroughly.
2. Filter out irrelevant or low-value comments.
3. Categorize relevant comments into meaningful groups.
4. Summarize the key insights from each category.
5. Identify actionable feedback for the content creator.

Output Format:
For each category, provide:
- Category Name: A concise label for the group of comments
- Summary: A brief overview of the main points in this category
- Category Count: The number of comments in this category
- Key Insights: 2-3 bullet points highlighting the most important takeaways
- Representative Comments: 1-2 examples of comments that best illustrate the category

Possible Categories (use only if relevant, and add others as needed):
- Positive Feedback
- Constructive Criticism
- Content Suggestions
- Technical Feedback (e.g., audio/video quality)
- Questions from Viewers
- Engagement Indicators (e.g., sharing intentions, subscription mentions)
- Emotional Responses
- Comparisons to Other Content

Additional Instructions:
- Focus on insights that are actionable for the content creator.
- Highlight any emerging trends or patterns in the comments.
- If there are conflicting viewpoints, present both sides objectively.
- Note the relative prevalence of different types of comments if significant.

{format_instructions}

<|eot_id|><|start_header_id|>user<|end_header_id|>
COMMENTS:

{comments}

<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>""", input_variables=["format_instructions", "comments"], partial_variables={"format_instructions": self.parser.get_format_instructions()})

        # Generator
        self.generator = self.prompt | self.model | self.parser

    def get_comments_summary(self, comments) -> CommentCategories:
        results: CommentCategories = self.generator.invoke({"comments": comments})
        return results
    
class PromptOutput(BaseModel):
    response: str = Field(description="Response to the prompt by the user")

class PromptResponse:
    def __init__(self):
        # Load the environment variables
        load_dotenv()
        os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

        # self.model = ChatGroq(model="llama3-8b-8192", temperature=0)
        self.model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)

        self.parser = JsonOutputParser(pydantic_object=PromptOutput)

        self.prompt = PromptTemplate(
            template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are a Short Form Content Creator Assistant, specialized in analyzing and responding to queries about video comments. Your role is to provide valuable insights to content creators by filtering and organizing viewer feedback.

You will the following: 
- A summary of the video that a user wants to understand more about. 
- A summary of the comments of each video. 
- A prompt from the user, highlighting what he wants to learn. 

Importantly, the summary of the comments will be split into a categories. In each category, you will be given:
- Category Name: A concise label for the group of comments
- Summary: A brief overview of the main points in this category
- Category Count: The number of comments in this category
- Key Insights: 2-3 bullet points highlighting the most important takeaways
- Representative Comments: 1-2 examples of comments that best illustrate the categoryy 

ASSISTANT'S TASK: You are to answer the prompt given by the user. 

{format_instructions}

<|eot_id|><|start_header_id|>user<|end_header_id|>
COMMENTS SUMMARY:

{comments}

VIDEO SUMMARY: 

{videoSummary}

USER PROMPT: 

{userPrompt}

<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>""", input_variables=["format_instructions", "comments", "videoSummary", "userPrompt"], partial_variables={"format_instructions": self.parser.get_format_instructions()})

        # Generator
        self.generator = self.prompt | self.model | self.parser

    def get_prompt_response(self, comments, videoSummary, userPrompt) -> PromptOutput:
        results: PromptOutput = self.generator.invoke({"comments": comments, "videoSummary": videoSummary, "userPrompt": userPrompt})
        return results



from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from dotenv import load_dotenv
import os
import json

class VideoFeedbackAgent:
    def __init__(self):
        load_dotenv()
        os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

        self.fetch_title_url = "http://localhost:8000/videos/by_url/"

        prompt_template = PromptTemplate(
            input_variables=["video_summary", "comments_summary", "input", "chat_history"],
            template="""
            You are an AI assistant that provides feedback on videos based on their performance data and comments.

            The following is the performance data for the video:

            Video Summary: 
            {video_summary}

            Comments Summary:
            {comments_summary}

            Chat History:
            {chat_history}

            You have all the necessary information about the video, including its URL, title, and summary. Do not ask for the URL as it's already provided in the video summary.

            Human: {input}
            AI: Let's approach this step-by-step:
            """
        )

        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0)

        chain = prompt_template | llm | StrOutputParser()

        self.agent_with_chat_history = RunnableWithMessageHistory(
            chain,
            lambda session_id: ChatMessageHistory(session_id=session_id),
            input_messages_key="input",
            history_messages_key="chat_history",
        )

    def generate_feedback(self, video, comments, user_input, session_id, url):
        video_summary = f"Title: {video.title}\nURL: {url}"
        
        comments_summary = "\n\n".join([
            f"Category: {comment.comment_category}\n"
            f"Category Count: {comment.category_count}\n"
            f"Summary: {comment.summary}\n"
            f"Insights: {json.loads(comment.comment_insights)}\n"
            f"Representative Comments: {json.loads(comment.representative_comments)}"
            for comment in comments
        ])

        full_input = f"""
        Video Information:
        {video_summary}

        Comments Summary:
        {comments_summary}

        Based on the above information about the video and its comments, please answer the following question:
        {user_input}

        Make sure to only answer questions related or relevant to the video based on the information provided.
        Do not provide any opinions or feedback that are not supported by the data.
        Politely decline if the question is not related to the video.
        If the user initiates small talk, politely redirect the conversation back to the video.
        Do not thank the user for providing the video information or comments summary as it is provided for your reference by the system.
        """

        response = self.agent_with_chat_history.invoke(
            {
                "video_summary": video_summary,
                "comments_summary": comments_summary,
                "input": full_input
            },
            config={"configurable": {"session_id": session_id}}
        )          

        print(response)
        return response 
    
    def _get_default_output_parser(self):
        return StrOutputParser()

    def create_prompt(self, **kwargs):
        return self.prompt_template

    @property
    def llm_prefix(self):
        return "AI Assistant: "

    @property
    def observation_prefix(self):
        return "Human: "

    @property
    def _agent_type(self):
        return "video-feedback-agent"

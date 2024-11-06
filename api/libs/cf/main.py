import os
from dotenv import load_dotenv
from api.libs.cf.tools.coinprofile import partna_tools
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.tools import DuckDuckGoSearchRun

# Load environment variables
load_dotenv()

dds = DuckDuckGoSearchRun()
cf_default_tools = [dds, *partna_tools]
cf_default_model: str = os.getenv("CONTROLFLOW_DEFAULT_LLM_MODEL")


class ControlFlow:
    def __init__(self, model: str = cf_default_model, tools=None, name='BitRamp'):
        import controlflow as cf

        # Create a memory module for user preferences
        user_preferences = cf.Memory(
            key="user_preferences",
            instructions="Store and retrieve user preferences."
        )

        conversation_history = cf.Memory(
            key="conversation_history",
            instructions="Store and retrieve conversation history."
        )

        if isinstance(model, str):
            if model.startswith("openai"):
                model = ChatOpenAI(model=model.split("openai/")[1], cache=True, temperature=0.1)
            elif model.startswith("anthropic"):
                model = ChatAnthropic(model=model.split("anthropic/")[1], cache=True, temperature=0.1)
            else:
                raise ValueError(f"Unsupported model provider: {model}")

        if tools is None:
            tools = cf_default_tools

        cf.defaults.model = model
        cf.defaults.agent = cf.Agent(
            name=name,
            model=model,
            tools=tools,
            memories=[user_preferences, conversation_history]
        )

        self.model = model
        self.tools = tools
        self.cf = cf

    def get_agent(self):
        return self.agent

    def get_model(self):
        return self.model

    def init(self):
        return self.cf
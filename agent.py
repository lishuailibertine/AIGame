# pip install -qU deepagents
import os
from dotenv import load_dotenv
from deepagents import create_deep_agent
from langchain.chat_models import init_chat_model
from skill_manager import load_skills, get_skill_paths, get_skills_files_dict
from deepagents.backends.utils import create_file_data
# Load environment variables from .env file
load_dotenv()


class AIAgent:
    """Encapsulated AI Agent for conversation"""

    def __init__(self, api_key=None,
                 model_name=None,
                 system_prompt=None):
        """Initialize the agent with model and system prompt"""
        # Use provided values or fall back to environment variables
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        self.model_name = model_name or os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

        if system_prompt is None:
            self.system_prompt = """You are a helpful assistant that provides weather information. You can use the get_weather tool to get the current weather for any city. When a user asks about the weather, use the get_weather function to retrieve the information and respond with the result."""
        else:
            self.system_prompt = system_prompt

        self._init_agent()

    def _init_agent(self):
        """Initialize the deepagents agent"""
        try:
            model = init_chat_model(
                model=self.model_name,
                model_provider="deepseek",
                api_key=self.api_key,
            )

            # Load skills from workspace (DeepAgents format)
            skills_paths = get_skill_paths()  # ["/skills/skill1/", "/skills/skill2/", ...]
            skills_files = get_skills_files_dict()  # {"/skills/skill1/SKILL.md": "content", ...}

            # Debug: Print skills info
            print(f"[DEBUG] Skills paths: {skills_paths}")
            print(f"[DEBUG] Skills files dict: {skills_files}")

            # Convert to create_file_data format
            skills_files_data = {}
            for path, content in skills_files.items():
                skills_files_data[path] = create_file_data(content)

            self.agent = create_deep_agent(
                model=model,
                tools=[],
                system_prompt=self.system_prompt,
                subagents=[],
                skills=skills_paths,
            )

            # Store skills files for later use in invoke (with create_file_data format)
            self.skills_files = skills_files_data
        except Exception as e:
            self.agent = None
            self.skills_files = {}
            raise RuntimeError(f"Failed to initialize agent: {str(e)}")

    def chat(self, message):
        """Send a message to the agent and get a response"""
        if self.agent is None:
            raise RuntimeError("Agent not initialized")

        try:
            # Prepare invoke parameters
            invoke_params = {
                "messages": [{"role": "user", "content": message}],
                "stream": False
            }

            # Add skills files if available
            if self.skills_files:
                invoke_params["files"] = self.skills_files

            result = self.agent.invoke(invoke_params)

            # Handle different response formats
            if isinstance(result, dict) and 'messages' in result:
                # Extract the last AIMessage content
                messages = result['messages']
                for msg in reversed(messages):
                    if hasattr(msg, 'content') and hasattr(msg, '__class__') and 'AIMessage' in msg.__class__.__name__:
                        return msg.content
            elif hasattr(result, 'content'):
                return result.content
            else:
                return str(result)
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            print(f"[ERROR] {error_detail}")
            return f"Error: {str(e)}"


# Global agent instance
_agent = None


def init_agent(api_key=None,
               model_name=None,
               system_prompt=None):
    """Initialize the global agent"""
    global _agent
    _agent = AIAgent(api_key=api_key, model_name=model_name, system_prompt=system_prompt)


def chat(message):
    """Send a message and get response from the agent"""
    global _agent
    if _agent is None:
        init_agent()
    return _agent.chat(message)


if __name__ == "__main__":
    # Example usage
    init_agent()
    result = chat("在吗？")
    print(f"Agent: {result}")

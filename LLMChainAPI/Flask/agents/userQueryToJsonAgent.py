import configparser
from os import path
from langchain.agents import initialize_agent, AgentType
from vertexai.generative_models import GenerationConfig, GenerativeModel
from langchain_google_vertexai import VertexAI
from tools.tools import getCountries, getFlows, getProductionValues, getProducts, getYears

current_dir = path.dirname(__file__)
config = configparser.ConfigParser()
config_file_path = path.join(current_dir, "..", "config.ini")
config.read(config_file_path)

project_id = config.get("DEFAULT", "PROJECT_ID")
location = config.get("DEFAULT", "LOCATION")
model_name = config.get("DEFAULT", "MODEL_NAME")

base_url = config.get("DEFAULT", "BASE_URL")

llm = VertexAI(model_name=model_name, max_output_tokens=1000)

agent = initialize_agent(tools=[getYears, getCountries, getFlows, getProductionValues, getProducts], llm=llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

agent.invoke("Who earns the most by selling petrol?")
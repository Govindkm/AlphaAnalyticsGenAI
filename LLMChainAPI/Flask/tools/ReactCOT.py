import configparser
from operator import itemgetter
from os import path
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain.llms import vertexai as langchainvertexai
from langchain.tools import StructuredTool
from langchain.agents import AgentType, initialize_agent, load_tools
from tools import getCountries, getFlows, getProductionValues, getProducts, getSummary, getYears
import vertexai

current_dir = path.dirname(__file__)
config = configparser.ConfigParser()
config_file_path = path.join(current_dir, "..", "config.ini")
config.read(config_file_path)

project_id = config.get("DEFAULT", "PROJECT_ID")
location = config.get("DEFAULT", "LOCATION")
model_name = config.get("DEFAULT", "MODEL_NAME")

vertexai.init(project=project_id, location=location)

structuredtools = [StructuredTool.from_function(getProductionValues), StructuredTool.from_function(getSummary)]

llm = langchainvertexai.VertexAI(model_name=model_name, max_output_tokens=1000)

agent = initialize_agent(structuredtools, llm, agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION, verbose=True, return_intermediate_steps = True)

def processWithReAct(user_query: str):
    """Uses Reasoning and Action prompts to process user query

    Args:
        user_query (str): returns nothing
    """
    
    output =  agent(user_query)
    return output
    # Placeholder code to process the user query and retrieve data
    # Here, you would implement your logic to obtain data from various APIs or sources
    
    
    
    # Placeholder data for demonstration
    data_from_country_api = [...]  # Data obtained from the country API
    data_from_value_api = [...]    # Data obtained from the value API
    data_from_flow_api = [...]     # Data obtained from the flow API
    images_data = [...]            # Image URLs or data
    summary_text = "Placeholder text summary of data obtained"
    table_id = "tableid"          # Placeholder table ID
    
    # Determine the status based on whether data retrieval was successful
    status = "success"  # or "fail" based on actual logic
    
    # Construct the JSON response
    response = {
        "status": status,
        "summary": summary_text,
        "data": {
            "countryapi": data_from_country_api,
            "valueapi": data_from_value_api,
            "flowapi": data_from_flow_api
        },
        "images": images_data,
        "tableid": table_id
    }
    
    return response

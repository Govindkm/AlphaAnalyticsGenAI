import configparser
from typing import Dict, Union
import vertexai
from langchain_community.llms import VertexAI
from langchain.tools import StructuredTool
from langchain_community import agent_toolkits
from vertexai.generative_models import GenerationConfig, GenerativeModel
from langchain_core.tools import tool
import requests


config = configparser.ConfigParser()
config.read("config.ini")


project_id = config.get("DEFAULT", "PROJECT_ID")
location = config.get("DEFAULT", "LOCATION")
model_name = config.get("DEFAULT", "MODEL_NAME")

base_url = config.get("DEFAULT", "BASE_URL")

vertexai.init(project=project_id, location=location)

model = GenerativeModel(model_name)

def getCountries(input_text: str) -> Union[str, Dict]:
    """
    Calls the countries API with the provided user query converted to appropriate odata query and returns the json response to get details of required countries.

    Args:
      input_text: The user query to be used in the API call.

    Returns:
      The raw API response in json format.
    """
    # ... (Optional) Preprocess the user query before making the API call
    # For example, extract relevant keywords or entities
    prompt = """Given OData supported {base_url}/countries API get endpoint returns countries data json in the format with countryId and countryName. 
    Return odata query if required based on user query. 
    
    Example 1:
    User Query: I need details of all the countries starting in alphabetic order    
    Output: $orderby=countryName
    Example 2:
    User Query: I need to find countryId for United States
    Output: $filter=countryName eq 'United States'
    Example 3:
    User Query: I need to get countries starting with letter p
    Output: $filter=startswith(tolower(countryName), 'p')
    User Query: """ + input_text + """
    Output: 
    """
    generation_config = GenerationConfig(
        temperature=0, max_output_tokens=1024, top_k=40, top_p=0.8)
    odataQuery = model.generate_content(prompt, generation_config=generation_config)
    
    print(odataQuery.text)
    # Construct the API request URL (you can modify based on API requirements)
    url = f"{base_url}/api/countries?{odataQuery.text}"  # Replace with appropriate URL structure
    # Build the request headers (add API key if provided)
    print(url)
    # ... Use appropriate library (e.g., requests) to make the API call
    # Replace with your preferred library and error handling
    
    jsonData = requests.get(url, verify=False)
    
    # ... Parse the API response based on its format (JSON, text, etc.)
    # You can use libraries like `json` or custom parsing logic

    response_data = jsonData.text # ... (parsed response data)  # Replace with actual parsing

    return response_data

print(getCountries("all the countries starting with letter a or p"))